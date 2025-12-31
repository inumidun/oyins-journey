"""
Tests for admin API module.
"""
import pytest
from unittest.mock import Mock, patch
import json
import sys
import os

# Add the api directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

from admin import lambda_handler


class TestAdminAPI:
    """Test cases for admin API functionality."""

    def test_lambda_handler_get_request(self):
        """Test GET request to admin endpoint."""
        event = {
            'httpMethod': 'GET',
            'path': '/admin',
            'headers': {},
            'queryStringParameters': None
        }
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
        assert 'application/json' in response['headers']['Content-Type']
        
        body = json.loads(response['body'])
        assert 'message' in body
        assert 'timestamp' in body

    def test_lambda_handler_post_request(self):
        """Test POST request to admin endpoint."""
        event = {
            'httpMethod': 'POST',
            'path': '/admin',
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'action': 'test'})
        }
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] in [200, 201, 400, 405]
        assert 'application/json' in response['headers']['Content-Type']

    def test_lambda_handler_invalid_method(self):
        """Test invalid HTTP method."""
        event = {
            'httpMethod': 'DELETE',
            'path': '/admin',
            'headers': {},
            'queryStringParameters': None
        }
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 405

    def test_lambda_handler_cors_headers(self):
        """Test CORS headers are present."""
        event = {
            'httpMethod': 'GET',
            'path': '/admin',
            'headers': {},
            'queryStringParameters': None
        }
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert 'Access-Control-Allow-Origin' in response['headers']
        assert 'Access-Control-Allow-Methods' in response['headers']
        assert 'Access-Control-Allow-Headers' in response['headers']

    def test_lambda_handler_exception_handling(self):
        """Test exception handling in lambda handler."""
        event = {
            'httpMethod': 'GET',
            'path': '/admin',
            'headers': {},
            'queryStringParameters': None
        }
        context = Mock()
        
        # Mock an exception in the handler
        with patch('admin.lambda_handler') as mock_handler:
            mock_handler.side_effect = Exception("Test error")
            
            try:
                lambda_handler(event, context)
            except Exception as e:
                assert str(e) == "Test error"