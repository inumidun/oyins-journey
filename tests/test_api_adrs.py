"""
Tests for ADRs API module.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import json
import sys
import os

# Set AWS region for tests
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"

# Add the api directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

from adrs import lambda_handler


class TestADRsAPI:
    """Test cases for ADRs API functionality."""

    @patch('adrs.boto3')
    def test_lambda_handler_get_all_adrs(self, mock_boto3):
        """Test GET request to retrieve all ADRs."""
        # Mock DynamoDB response
        mock_dynamodb = MagicMock()
        mock_table = MagicMock()
        mock_boto3.resource.return_value = mock_dynamodb
        mock_dynamodb.Table.return_value = mock_table
        
        mock_table.scan.return_value = {
            'Items': [
                {
                    'id': 'adr-001',
                    'title': 'Use React for Frontend',
                    'status': 'accepted',
                    'date': '2024-01-15',
                    'context': 'We need a modern frontend framework',
                    'decision': 'Use React with TypeScript',
                    'consequences': 'Better developer experience'
                }
            ]
        }
        
        event = {
            'httpMethod': 'GET',
            'path': '/adrs',
            'headers': {},
            'queryStringParameters': None
        }
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'adrs' in body
        assert len(body['adrs']) == 1
        assert body['adrs'][0]['id'] == 'adr-001'

    @patch('adrs.boto3')
    def test_lambda_handler_get_adr_by_status(self, mock_boto3):
        """Test GET request with status filter."""
        mock_dynamodb = MagicMock()
        mock_table = MagicMock()
        mock_boto3.resource.return_value = mock_dynamodb
        mock_dynamodb.Table.return_value = mock_table
        
        mock_table.scan.return_value = {
            'Items': [
                {
                    'id': 'adr-001',
                    'title': 'Use React for Frontend',
                    'status': 'accepted',
                    'date': '2024-01-15'
                }
            ]
        }
        
        event = {
            'httpMethod': 'GET',
            'path': '/adrs',
            'headers': {},
            'queryStringParameters': {'status': 'accepted'}
        }
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert len(body['adrs']) == 1
        assert body['adrs'][0]['status'] == 'accepted'

    @patch('adrs.boto3')
    def test_lambda_handler_dynamodb_error(self, mock_boto3):
        """Test DynamoDB error handling."""
        mock_dynamodb = MagicMock()
        mock_table = MagicMock()
        mock_boto3.resource.return_value = mock_dynamodb
        mock_dynamodb.Table.return_value = mock_table
        
        mock_table.scan.side_effect = Exception("DynamoDB error")
        
        event = {
            'httpMethod': 'GET',
            'path': '/adrs',
            'headers': {},
            'queryStringParameters': None
        }
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 500
        body = json.loads(response['body'])
        assert 'error' in body

    def test_lambda_handler_invalid_method(self):
        """Test invalid HTTP method."""
        event = {
            'httpMethod': 'POST',
            'path': '/adrs',
            'headers': {},
            'queryStringParameters': None
        }
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 405

    @patch('adrs.boto3')
    def test_lambda_handler_empty_result(self, mock_boto3):
        """Test empty ADRs result."""
        mock_dynamodb = MagicMock()
        mock_table = MagicMock()
        mock_boto3.resource.return_value = mock_dynamodb
        mock_dynamodb.Table.return_value = mock_table
        
        mock_table.scan.return_value = {'Items': []}
        
        event = {
            'httpMethod': 'GET',
            'path': '/adrs',
            'headers': {},
            'queryStringParameters': None
        }
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['adrs'] == []

    def test_lambda_handler_cors_headers(self):
        """Test CORS headers are present."""
        event = {
            'httpMethod': 'GET',
            'path': '/adrs',
            'headers': {},
            'queryStringParameters': None
        }
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert 'Access-Control-Allow-Origin' in response['headers']
        assert 'Access-Control-Allow-Methods' in response['headers']
        assert 'Access-Control-Allow-Headers' in response['headers']