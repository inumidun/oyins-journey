"""
Property-based tests for certifications functionality.
Feature: living-architecture-resume-enhancement
"""

import pytest
import json
from datetime import datetime, timedelta
from hypothesis import given, strategies as st, settings
from moto import mock_dynamodb
import boto3
import os
import sys
import uuid

# Set AWS region for tests
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"

# Set environment variable before importing
os.environ['CERTIFICATIONS_TABLE'] = 'test-certifications'

# Add the api directory to the path so we can import the Lambda function
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'infrastructure', 'modules', 'lambda', 'codes', 'certifications'))

# Mock DynamoDB before importing the module
with mock_dynamodb():
    # Create a temporary table for import
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    temp_table = dynamodb.create_table(
        TableName='test-certifications',
        KeySchema=[{'AttributeName': 'cert_id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'cert_id', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )
    
    from certifications import lambda_handler


# Strategies for generating test data
@st.composite
def certification_data(draw):
    """Generate valid certification data."""
    providers = ['AWS', 'Azure', 'GCP', 'Other']
    categories = ['cloud', 'security', 'devops', 'data']
    
    # Generate dates
    issue_date = draw(st.dates(min_value=datetime(2020, 1, 1).date(), 
                              max_value=datetime.now().date()))
    
    # Some certifications have expiry dates, some don't
    has_expiry = draw(st.booleans())
    expiry_date = None
    if has_expiry:
        expiry_date = draw(st.dates(min_value=issue_date, 
                                   max_value=issue_date + timedelta(days=1095)))  # 3 years max
    
    # Generate unique cert_id using UUID to avoid conflicts
    unique_id = str(uuid.uuid4())[:8]
    
    return {
        'cert_id': f"test-cert-{unique_id}",
        'name': draw(st.text(min_size=10, max_size=50, alphabet=st.characters(min_codepoint=32, max_codepoint=126))),
        'provider': draw(st.sampled_from(providers)),
        'category': draw(st.sampled_from(categories)),
        'issue_date': issue_date.strftime('%Y-%m-%d'),
        'expiry_date': expiry_date.strftime('%Y-%m-%d') if expiry_date else None,
        'credential_id': draw(st.text(min_size=5, max_size=20, alphabet=st.characters(min_codepoint=48, max_codepoint=90))),
        'verification_url': f"https://verify.example.com/{unique_id}",
        'badge_url': f"https://badges.example.com/{unique_id}.png"
    }


class TestCertificationDataIntegrity:
    """Test certification data integrity properties."""
    
    def setup_method(self, method):
        """Set up test environment with fresh table."""
        # Create unique table name for each test
        self.table_name = f'test-certifications-{uuid.uuid4().hex[:8]}'
        os.environ['CERTIFICATIONS_TABLE'] = self.table_name
        
        # Create mock DynamoDB table
        self.mock = mock_dynamodb()
        self.mock.start()
        
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=[
                {'AttributeName': 'cert_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'cert_id', 'AttributeType': 'S'},
                {'AttributeName': 'provider', 'AttributeType': 'S'},
                {'AttributeName': 'category', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'ProviderIndex',
                    'KeySchema': [
                        {'AttributeName': 'provider', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'}
                },
                {
                    'IndexName': 'CategoryIndex',
                    'KeySchema': [
                        {'AttributeName': 'category', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'}
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
    
    def teardown_method(self, method):
        """Clean up after each test."""
        self.mock.stop()
    
    @given(st.lists(certification_data(), min_size=1, max_size=3))
    @settings(max_examples=5)
    def test_certification_data_integrity(self, certifications):
        """
        Property 1: Certification Data Integrity
        For any certification dataset, all returned certifications should contain 
        complete metadata (name, issuer, dates, verification link) and correct 
        expiration status based on current date.
        
        **Feature: living-architecture-resume-enhancement, Property 1: Certification Data Integrity**
        **Validates: Requirements 1.1, 1.2, 1.3**
        """
        # Populate table with test data
        for cert in certifications:
            self.table.put_item(Item=cert)
        
        # Call the Lambda function
        event = {'queryStringParameters': None}
        response = lambda_handler(event, None)
        
        # Verify response structure
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        
        # Verify all certifications are returned
        returned_certs = body['certifications']
        assert len(returned_certs) == len(certifications)
        
        # Verify data integrity for each certification
        current_date = datetime.now().date()
        
        for cert in returned_certs:
            # Verify required fields are present
            required_fields = ['cert_id', 'name', 'provider', 'category', 'issue_date', 
                             'credential_id', 'verification_url']
            for field in required_fields:
                assert field in cert, f"Required field {field} missing from certification"
                assert cert[field] is not None, f"Required field {field} is None"
                assert cert[field] != "", f"Required field {field} is empty"
            
            # Verify computed status is correctly calculated
            assert 'computed_status' in cert, "computed_status field missing"
            
            if cert.get('expiry_date'):
                expiry = datetime.strptime(cert['expiry_date'], '%Y-%m-%d').date()
                if expiry < current_date:
                    assert cert['computed_status'] == 'expired'
                elif expiry < current_date + timedelta(days=90):
                    assert cert['computed_status'] == 'expiring_soon'
                else:
                    assert cert['computed_status'] == 'active'
            else:
                assert cert['computed_status'] == 'no_expiry'
            
            # Verify URL format
            assert cert['verification_url'].startswith('http'), "Invalid verification URL format"
            if cert.get('badge_url'):
                assert cert['badge_url'].startswith('http'), "Invalid badge URL format"

    @given(st.lists(certification_data(), min_size=2, max_size=4))
    @settings(max_examples=5)
    def test_certification_filtering_accuracy(self, certifications):
        """
        Property 2: Certification Filtering Accuracy
        For any provider filter (AWS, Azure, GCP), the returned certifications 
        should only include items matching that specific provider.
        
        **Feature: living-architecture-resume-enhancement, Property 2: Certification Filtering Accuracy**
        **Validates: Requirements 1.4**
        """
        # Populate table with test data
        for cert in certifications:
            self.table.put_item(Item=cert)
        
        # Get unique providers from test data
        providers_in_data = list(set(cert['provider'] for cert in certifications))
        
        # Test filtering for each provider that exists in the data
        for provider in providers_in_data:
            event = {
                'queryStringParameters': {
                    'provider': provider
                }
            }
            response = lambda_handler(event, None)
            
            # Verify response structure
            assert response['statusCode'] == 200
            body = json.loads(response['body'])
            
            returned_certs = body['certifications']
            
            # Verify all returned certifications match the provider filter
            for cert in returned_certs:
                assert cert['provider'] == provider, f"Certification with provider {cert['provider']} returned when filtering for {provider}"
            
            # Verify count matches expected
            expected_count = len([c for c in certifications if c['provider'] == provider])
            assert len(returned_certs) == expected_count, f"Expected {expected_count} certifications for provider {provider}, got {len(returned_certs)}"
        
        # Test with non-existent provider
        event = {
            'queryStringParameters': {
                'provider': 'NonExistentProvider'
            }
        }
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert len(body['certifications']) == 0, "Should return empty list for non-existent provider"