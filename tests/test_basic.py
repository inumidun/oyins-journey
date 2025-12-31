"""
Basic tests that don't require AWS mocking.
"""
import pytest
import os
import json
from datetime import datetime


class TestBasic:
    """Basic tests without AWS dependencies."""

    def test_environment_setup(self):
        """Test that the test environment is properly configured."""
        assert os.environ.get("AWS_DEFAULT_REGION") == "us-east-1"
        assert os.environ.get("AWS_ACCESS_KEY_ID") == "testing"
        assert os.environ.get("AWS_SECRET_ACCESS_KEY") == "testing"

    def test_json_serialization(self):
        """Test JSON serialization works correctly."""
        test_data = {
            "id": "test-123",
            "name": "Test Item",
            "timestamp": datetime.now().isoformat(),
            "active": True,
            "count": 42
        }
        
        # Should serialize and deserialize without issues
        json_str = json.dumps(test_data)
        parsed_data = json.loads(json_str)
        
        assert parsed_data["id"] == test_data["id"]
        assert parsed_data["name"] == test_data["name"]
        assert parsed_data["active"] == test_data["active"]
        assert parsed_data["count"] == test_data["count"]

    def test_lambda_event_structure(self):
        """Test Lambda event structure validation."""
        event = {
            'httpMethod': 'GET',
            'path': '/test',
            'headers': {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            'queryStringParameters': {
                'param1': 'value1',
                'param2': 'value2'
            },
            'body': None
        }
        
        # Validate event structure
        assert event['httpMethod'] in ['GET', 'POST', 'PUT', 'DELETE']
        assert event['path'].startswith('/')
        assert 'Content-Type' in event['headers']
        assert isinstance(event['queryStringParameters'], dict)

    def test_lambda_response_structure(self):
        """Test Lambda response structure validation."""
        response = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            },
            'body': json.dumps({
                'message': 'Success',
                'data': {'id': 'test-123', 'name': 'Test Item'}
            })
        }
        
        # Validate response structure
        assert response['statusCode'] == 200
        assert 'Content-Type' in response['headers']
        assert 'Access-Control-Allow-Origin' in response['headers']
        
        # Validate body is valid JSON
        body_data = json.loads(response['body'])
        assert 'message' in body_data
        assert 'data' in body_data

    def test_certification_data_validation(self):
        """Test certification data structure validation."""
        certification = {
            "id": "aws-saa-c03-2024",
            "name": "AWS Solutions Architect Associate",
            "provider": "AWS",
            "category": "cloud",
            "issue_date": "2024-01-15",
            "expiry_date": "2027-01-15",
            "credential_id": "ABC123XYZ",
            "computed_status": "active"
        }
        
        # Validate required fields
        required_fields = ["id", "name", "provider", "issue_date"]
        for field in required_fields:
            assert field in certification
            assert certification[field] is not None
            assert len(str(certification[field])) > 0
        
        # Validate provider is valid
        valid_providers = ["AWS", "Azure", "GCP", "Other"]
        assert certification["provider"] in valid_providers
        
        # Validate status is valid
        valid_statuses = ["active", "expired", "expiring_soon", "no_expiry"]
        assert certification["computed_status"] in valid_statuses

    def test_skill_data_validation(self):
        """Test skill data structure validation."""
        skill = {
            "id": "python-programming",
            "name": "Python",
            "category": "programming",
            "proficiency": "advanced",
            "years_experience": 5,
            "usage_count": 25
        }
        
        # Validate required fields
        required_fields = ["id", "name", "category"]
        for field in required_fields:
            assert field in skill
            assert skill[field] is not None
            assert len(str(skill[field])) > 0
        
        # Validate proficiency level
        valid_proficiency = ["beginner", "intermediate", "advanced", "expert"]
        assert skill["proficiency"] in valid_proficiency
        
        # Validate numeric fields
        assert isinstance(skill["years_experience"], int)
        assert skill["years_experience"] >= 0
        assert isinstance(skill["usage_count"], int)
        assert skill["usage_count"] >= 0

    def test_project_data_validation(self):
        """Test project data structure validation."""
        project = {
            "id": "living-architecture-resume",
            "name": "Living Architecture Resume",
            "description": "A deployed cloud system that serves as a queryable CV",
            "status": "active",
            "technologies": ["Python", "AWS", "React", "TypeScript"],
            "start_date": "2024-01-01"
        }
        
        # Validate required fields
        required_fields = ["id", "name", "description", "status"]
        for field in required_fields:
            assert field in project
            assert project[field] is not None
            assert len(str(project[field])) > 0
        
        # Validate status
        valid_statuses = ["active", "completed", "planned", "on_hold"]
        assert project["status"] in valid_statuses
        
        # Validate technologies is a list
        assert isinstance(project["technologies"], list)
        assert len(project["technologies"]) > 0