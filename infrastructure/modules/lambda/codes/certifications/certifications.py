import json
import boto3
import os
import logging
from typing import Dict, Any, List
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('CERTIFICATIONS_TABLE')

if not table_name:
    logger.error("CERTIFICATIONS_TABLE environment variable not set")
    raise ValueError("CERTIFICATIONS_TABLE environment variable is required")

certifications_table = dynamodb.Table(table_name)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for certifications API endpoints.
    
    Supports:
    - GET /certifications - List all certifications
    - GET /certifications?provider={provider} - Filter by provider
    - GET /certifications?status={status} - Filter by status
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response
    """
    try:
        # Log the incoming request
        logger.info(f"Processing request: {json.dumps(event, default=str)}")
        
        # Parse query parameters
        query_params = event.get('queryStringParameters') or {}
        provider_filter = query_params.get('provider')
        status_filter = query_params.get('status')
        
        # Get all certifications
        response = certifications_table.scan()
        certifications = response.get('Items', [])
        
        # Apply filters
        if provider_filter:
            certifications = [c for c in certifications if c.get('provider', '').lower() == provider_filter.lower()]
        
        if status_filter:
            certifications = [c for c in certifications if c.get('status', '').lower() == status_filter.lower()]
        
        # Sort by earned_date (newest first)
        certifications.sort(key=lambda x: x.get('earned_date', ''), reverse=True)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'certifications': certifications,
                'count': len(certifications),
                'filters': {
                    'provider': provider_filter,
                    'status': status_filter
                }
            })
        }
        
    except ClientError as e:
        logger.error(f"DynamoDB error: {e}")
        return _error_response(500, "Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return _error_response(500, "Internal server error")

def _error_response(status_code: int, message: str) -> Dict[str, Any]:
    """
    Create standardized error response.
    
    Args:
        status_code: HTTP status code
        message: Error message
        
    Returns:
        API Gateway error response
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'error': message,
            'timestamp': 'context.aws_request_id'
        })
    }