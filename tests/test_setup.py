"""
Basic setup tests to verify the testing environment is working correctly.
"""
import pytest
import os
import boto3
from moto.dynamodb import mock_dynamodb
from moto.cloudwatch import mock_cloudwatch


class TestSetup:
    """Basic setup and configuration tests."""

    def test_aws_credentials_set(self):
        """Test that AWS credentials are properly set."""
        assert os.environ.get("AWS_DEFAULT_REGION") == "us-east-1"
        assert os.environ.get("AWS_ACCESS_KEY_ID") == "testing"
        assert os.environ.get("AWS_SECRET_ACCESS_KEY") == "testing"

    @mock_dynamodb
    def test_dynamodb_mock_works(self):
        """Test that DynamoDB mocking is working."""
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
        # Create a test table
        table = dynamodb.create_table(
            TableName='test-table',
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        
        # Verify table was created
        assert table.table_name == 'test-table'
        
        # Test basic operations
        table.put_item(Item={'id': 'test-id', 'name': 'test-item'})
        response = table.get_item(Key={'id': 'test-id'})
        
        assert 'Item' in response
        assert response['Item']['name'] == 'test-item'

    @mock_cloudwatch
    def test_cloudwatch_mock_works(self):
        """Test that CloudWatch mocking is working."""
        cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
        
        # Test putting a metric
        response = cloudwatch.put_metric_data(
            Namespace='TestNamespace',
            MetricData=[
                {
                    'MetricName': 'TestMetric',
                    'Value': 1.0,
                    'Unit': 'Count'
                }
            ]
        )
        
        # Should not raise an exception
        assert response['ResponseMetadata']['HTTPStatusCode'] == 200

    def test_pytest_fixtures_available(self, sample_certification, sample_skill, sample_project):
        """Test that pytest fixtures are working."""
        assert sample_certification['id'] == 'aws-saa-c03-2024'
        assert sample_skill['name'] == 'Python'
        assert sample_project['name'] == 'Living Architecture Resume'

    def test_lambda_context_fixture(self, lambda_context):
        """Test that Lambda context fixture is working."""
        assert lambda_context.function_name == 'test-function'
        assert lambda_context.memory_limit_in_mb == 128
        assert callable(lambda_context.remaining_time_in_millis)

    def test_api_event_fixture(self, api_event):
        """Test that API event fixture is working."""
        assert api_event['httpMethod'] == 'GET'
        assert api_event['path'] == '/test'
        assert 'Content-Type' in api_event['headers']