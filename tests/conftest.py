"""
Pytest configuration and fixtures for the Living Architecture Resume test suite.
"""
import pytest
import os
import boto3

# Try different moto import patterns for compatibility
try:
    from moto import mock_dynamodb, mock_cloudwatch
except ImportError:
    try:
        from moto.dynamodb import mock_dynamodb
        from moto.cloudwatch import mock_cloudwatch
    except ImportError:
        # Fallback for very old versions
        from moto.mock_dynamodb2 import mock_dynamodb2 as mock_dynamodb
        from moto.mock_cloudwatch import mock_cloudwatch


@pytest.fixture(scope="session", autouse=True)
def aws_credentials():
    """Set up AWS credentials for testing."""
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def dynamodb_mock():
    """Mock DynamoDB for testing."""
    with mock_dynamodb():
        yield boto3.resource('dynamodb', region_name='us-east-1')


@pytest.fixture
def cloudwatch_mock():
    """Mock CloudWatch for testing."""
    with mock_cloudwatch():
        yield boto3.client('cloudwatch', region_name='us-east-1')


@pytest.fixture
def sample_certification():
    """Sample certification data for testing."""
    return {
        "id": "aws-saa-c03-2024",
        "name": "AWS Solutions Architect Associate",
        "provider": "AWS",
        "category": "cloud",
        "issue_date": "2024-01-15",
        "expiry_date": "2027-01-15",
        "credential_id": "ABC123XYZ",
        "verification_url": "https://aws.amazon.com/verification/ABC123XYZ",
        "computed_status": "active"
    }


@pytest.fixture
def sample_skill():
    """Sample skill data for testing."""
    return {
        "id": "python-programming",
        "name": "Python",
        "category": "programming",
        "proficiency": "advanced",
        "years_experience": 5,
        "usage_count": 25,
        "technologies": ["FastAPI", "Django", "Flask"]
    }


@pytest.fixture
def sample_project():
    """Sample project data for testing."""
    return {
        "id": "living-architecture-resume",
        "name": "Living Architecture Resume",
        "description": "A deployed cloud system that serves as a queryable CV",
        "status": "active",
        "technologies": ["Python", "AWS", "React", "TypeScript"],
        "start_date": "2024-01-01",
        "repository": "https://github.com/user/living-architecture-resume",
        "live_url": "https://oyins-journey.dev"
    }


@pytest.fixture
def api_event():
    """Sample API Gateway event for Lambda testing."""
    return {
        'httpMethod': 'GET',
        'path': '/test',
        'headers': {
            'Content-Type': 'application/json'
        },
        'queryStringParameters': None,
        'body': None
    }


@pytest.fixture
def lambda_context():
    """Mock Lambda context for testing."""
    class MockContext:
        def __init__(self):
            self.function_name = "test-function"
            self.function_version = "$LATEST"
            self.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test-function"
            self.memory_limit_in_mb = 128
            self.remaining_time_in_millis = lambda: 30000
            self.log_group_name = "/aws/lambda/test-function"
            self.log_stream_name = "2024/12/31/[$LATEST]test123"
            self.aws_request_id = "test-request-id"
    
    return MockContext()