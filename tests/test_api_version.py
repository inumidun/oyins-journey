"""
Tests for version API module.
"""
import pytest
from unittest.mock import Mock, patch
import json
import sys
import os

# Add the api directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

from version import lambda_handler


class TestVersionAPI:
    """Test cases for version API functionality."""

    def test_lambda_handler_get_version(self):
        """Test GET request to version endpoint."""
        event = {
            'httpMethod': 'GET',
            'path': '/version',
            'headers': {},
            'queryStringParameters': None
        }
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
        assert 'application/json' in response['headers']['Content-Type']
        
        body = json.loads(response['body'])
        assert 'version' in body
        assert 'build_date' in body
        assert 'commit_sha' in body

    def test_lambda_handler_version_format(self):
        """Test version format is correct."""
        event = {
            'httpMethod': 'GET',
            'path': '/version',
            'headers': {},
            'queryStringParameters': None
        }
        context = Mock()
        
        response = lambda_handler(event, context)
        body = json.loads(response['body'])
        
        # Version should be in semantic versioning format
        version = body['version']
        assert isinstance(version, str)
        assert len(version.split('.')) >= 2  # At least major.minor

    def test_lambda_handler_invalid_method(self):
        """Test invalid HTTP method."""
        event = {
            'httpMethod': 'POST',
            'path': '/version',
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
            'path': '/version',
            'headers': {},
            'queryStringParameters': None
        }
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert 'Access-Control-Allow-Origin' in response['headers']
        assert 'Access-Control-Allow-Methods' in response['headers']
        assert 'Access-Control-Allow-Headers' in response['headers']

    @patch('version.os.environ')
    def test_lambda_handler_environment_variables(self, mock_env):
        """Test environment variable handling."""
        mock_env.get.side_effect = lambda key, default=None: {
            'VERSION': '2.1.0',
            'BUILD_DATE': '2024-12-31',
            'COMMIT_SHA': 'abc123def456'
        }.get(key, default)
        
        event = {
            'httpMethod': 'GET',
            'path': '/version',
            'headers': {},
            'queryStringParameters': None
        }
        context = Mock()
        
        response = lambda_handler(event, context)
        body = json.loads(response['body'])
        
        assert body['version'] == '2.1.0'
        assert body['build_date'] == '2024-12-31'
        assert body['commit_sha'] == 'abc123def456'

    def test_lambda_handler_response_structure(self):
        """Test response structure is consistent."""
        event = {
            'httpMethod': 'GET',
            'path': '/version',
            'headers': {},
            'queryStringParameters': None
        }
        context = Mock()
        
        response = lambda_handler(event, context)
        body = json.loads(response['body'])
        
        # Required fields
        required_fields = ['version', 'build_date', 'commit_sha']
        for field in required_fields:
            assert field in body
            assert body[field] is not None