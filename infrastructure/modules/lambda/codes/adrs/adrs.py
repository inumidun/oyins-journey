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
table_name = os.environ.get('ADRS_TABLE')

if not table_name:
    logger.error("ADRS_TABLE environment variable not set")
    raise ValueError("ADRS_TABLE environment variable is required")

adrs_table = dynamodb.Table(table_name)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for Architecture Decision Records (ADRs) API.
    
    Supports:
    - GET /architecture/decisions - List all ADRs
    - GET /architecture/decisions?status={status} - Filter by status
    
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
        status_filter = query_params.get('status')
        
        # Get all ADRs
        response = adrs_table.scan()
        adrs = response.get('Items', [])
        
        # Apply status filter if specified
        if status_filter:
            adrs = [adr for adr in adrs if adr.get('status', '').lower() == status_filter.lower()]
        
        # Sort by date (newest first)
        adrs.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'adrs': adrs,
                'count': len(adrs),
                'filters': {
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