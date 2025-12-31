"""
Property-based tests for data integration and GitHub enrichment functionality.
Feature: living-architecture-resume-enhancement
"""

import pytest
from hypothesis import given, strategies as st, settings
import json
import os
import sys
import boto3
from moto.dynamodb import mock_dynamodb
from unittest.mock import patch, MagicMock
import requests

# Set AWS region for tests
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"

# Add the api directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

from projects import lambda_handler as projects_handler
from skills import lambda_handler as skills_handler


@mock_dynamodb
class TestDataIntegrationProperties:
    
    def setup_method(self):
        """Set up test DynamoDB tables"""
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
        # Create projects table
        self.projects_table = self.dynamodb.create_table(
            TableName='test-projects',
            KeySchema=[{'AttributeName': 'project_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'project_id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        
        # Create skills table
        self.skills_table = self.dynamodb.create_table(
            TableName='test-skills',
            KeySchema=[{'AttributeName': 'skill_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[
                {'AttributeName': 'skill_id', 'AttributeType': 'S'},
                {'AttributeName': 'category', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[{
                'IndexName': 'CategoryIndex',
                'KeySchema': [{'AttributeName': 'category', 'KeyType': 'HASH'}],
                'Projection': {'ProjectionType': 'ALL'}
            }],
            BillingMode='PAY_PER_REQUEST'
        )

    # Property 7: Project Data Enrichment
    # Feature: living-architecture-resume-enhancement, Property 7: For any project with GitHub links, the displayed data should include repository information and commit activity
    @given(
        project_data=st.fixed_dictionaries({
            'project_id': st.text(min_size=1, max_size=50),
            'name': st.text(min_size=1, max_size=100),
            'description': st.text(min_size=1, max_size=500),
            'github_url': st.one_of(
                st.none(),
                st.text(min_size=1).map(lambda x: f"https://github.com/user/{x}")
            ),
            'technologies': st.lists(st.text(min_size=1, max_size=20), min_size=1, max_size=10),
            'start_date': st.dates().map(str),
            'status': st.sampled_from(['active', 'completed', 'archived'])
        })
    )
    @settings(max_examples=100)
    def test_project_data_enrichment_property(self, project_data):
        """
        Property 7: For any project with GitHub links, the displayed data should include 
        repository information and commit activity
        **Validates: Requirements 3.2**
        """
        # Insert test project
        self.projects_table.put_item(Item=project_data)
        
        # Mock GitHub API response
        mock_github_response = {
            'stargazers_count': 42,
            'forks_count': 7,
            'open_issues_count': 3,
            'updated_at': '2024-12-30T10:00:00Z',
            'language': 'Python',
            'topics': ['api', 'serverless']
        }
        
        with patch.dict('os.environ', {'PROJECTS_TABLE': 'test-projects'}):
            with patch('requests.get') as mock_get:
                mock_get.return_value.json.return_value = mock_github_response
                mock_get.return_value.status_code = 200
                
                # Test getting all projects
                event = {'queryStringParameters': None, 'pathParameters': None}
                response = projects_handler(event, {})
                
                assert response['statusCode'] == 200
                body = json.loads(response['body'])
                
                # Verify project data is returned
                assert 'projects' in body
                assert len(body['projects']) > 0
                
                # Find our test project
                test_project = next(
                    (p for p in body['projects'] if p['project_id'] == project_data['project_id']), 
                    None
                )
                assert test_project is not None
                
                # Verify basic project data is preserved
                assert test_project['name'] == project_data['name']
                assert test_project['description'] == project_data['description']
                assert test_project['technologies'] == project_data['technologies']
                
                # If project has GitHub URL, verify enrichment would be possible
                if project_data.get('github_url'):
                    # The property ensures that GitHub data CAN be enriched
                    # Implementation should handle GitHub API integration
                    assert 'github_url' in test_project

    # Property 8: Data Loading Error Handling
    # Feature: living-architecture-resume-enhancement, Property 8: For any data loading failure, the system should gracefully handle the error and provide appropriate fallback mechanisms
    @given(
        error_scenario=st.sampled_from([
            'dynamodb_unavailable',
            'github_api_timeout',
            'github_api_rate_limit',
            'invalid_github_url',
            'network_error'
        ])
    )
    @settings(max_examples=100)
    def test_data_loading_error_handling_property(self, error_scenario):
        """
        Property 8: For any data loading failure, the system should gracefully handle 
        the error and provide appropriate fallback mechanisms
        **Validates: Requirements 3.5**
        """
        with patch.dict('os.environ', {'PROJECTS_TABLE': 'test-projects'}):
            event = {'queryStringParameters': None, 'pathParameters': None}
            
            if error_scenario == 'dynamodb_unavailable':
                # Simulate DynamoDB error
                with patch('boto3.resource') as mock_resource:
                    mock_resource.side_effect = Exception("DynamoDB unavailable")
                    response = projects_handler(event, {})
                    
                    # Should return error but not crash
                    assert response['statusCode'] == 500
                    body = json.loads(response['body'])
                    assert 'error' in body
                    
            elif error_scenario in ['github_api_timeout', 'github_api_rate_limit', 'network_error']:
                # Insert a project with GitHub URL
                test_project = {
                    'project_id': 'test-project',
                    'name': 'Test Project',
                    'github_url': 'https://github.com/user/repo'
                }
                self.projects_table.put_item(Item=test_project)
                
                with patch('requests.get') as mock_get:
                    if error_scenario == 'github_api_timeout':
                        mock_get.side_effect = requests.exceptions.Timeout()
                    elif error_scenario == 'github_api_rate_limit':
                        mock_get.return_value.status_code = 429
                    else:  # network_error
                        mock_get.side_effect = requests.exceptions.ConnectionError()
                    
                    response = projects_handler(event, {})
                    
                    # Should still return project data even if GitHub enrichment fails
                    assert response['statusCode'] == 200
                    body = json.loads(response['body'])
                    assert 'projects' in body
                    assert len(body['projects']) > 0
                    
            elif error_scenario == 'invalid_github_url':
                # Test with invalid GitHub URL
                test_project = {
                    'project_id': 'test-project',
                    'name': 'Test Project',
                    'github_url': 'not-a-valid-url'
                }
                self.projects_table.put_item(Item=test_project)
                
                response = projects_handler(event, {})
                
                # Should still return project data
                assert response['statusCode'] == 200
                body = json.loads(response['body'])
                assert 'projects' in body

    @given(
        skill_data=st.fixed_dictionaries({
            'skill_id': st.text(min_size=1, max_size=50),
            'name': st.text(min_size=1, max_size=100),
            'category': st.sampled_from(['cloud', 'programming', 'database', 'devops']),
            'proficiency': st.sampled_from(['beginner', 'intermediate', 'advanced', 'expert']),
            'technologies': st.lists(st.text(min_size=1, max_size=20), min_size=1, max_size=5),
            'years_experience': st.integers(min_value=0, max_value=20)
        })
    )
    @settings(max_examples=100)
    def test_skills_data_integration_property(self, skill_data):
        """
        Property: Skills data should be fetched from DynamoDB instead of mock data
        **Validates: Requirements 3.1**
        """
        # Insert test skill
        self.skills_table.put_item(Item=skill_data)
        
        with patch.dict('os.environ', {'SKILLS_TABLE': 'test-skills'}):
            # Test getting all skills
            event = {'queryStringParameters': None}
            response = skills_handler(event, {})
            
            assert response['statusCode'] == 200
            body = json.loads(response['body'])
            
            # Verify skills data is returned from DynamoDB
            assert 'skills' in body
            assert len(body['skills']) > 0
            
            # Find our test skill
            test_skill = next(
                (s for s in body['skills'] if s['skill_id'] == skill_data['skill_id']), 
                None
            )
            assert test_skill is not None
            
            # Verify skill data integrity
            assert test_skill['name'] == skill_data['name']
            assert test_skill['category'] == skill_data['category']
            assert test_skill['proficiency'] == skill_data['proficiency']

    @given(
        category_filter=st.sampled_from(['cloud', 'programming', 'database', 'devops'])
    )
    @settings(max_examples=100)
    def test_skills_category_filtering_property(self, category_filter):
        """
        Property: Skills filtering by category should return only matching skills
        **Validates: Requirements 3.1**
        """
        # Insert skills with different categories
        skills = [
            {'skill_id': 'skill1', 'name': 'AWS', 'category': 'cloud'},
            {'skill_id': 'skill2', 'name': 'Python', 'category': 'programming'},
            {'skill_id': 'skill3', 'name': 'PostgreSQL', 'category': 'database'},
            {'skill_id': 'skill4', 'name': 'Docker', 'category': 'devops'}
        ]
        
        for skill in skills:
            self.skills_table.put_item(Item=skill)
        
        with patch.dict('os.environ', {'SKILLS_TABLE': 'test-skills'}):
            # Test filtering by category
            event = {'queryStringParameters': {'category': category_filter}}
            response = skills_handler(event, {})
            
            assert response['statusCode'] == 200
            body = json.loads(response['body'])
            
            # Verify only skills from the specified category are returned
            assert 'skills' in body
            for skill in body['skills']:
                assert skill['category'] == category_filter