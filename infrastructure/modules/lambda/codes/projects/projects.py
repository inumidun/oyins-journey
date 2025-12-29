import json
import boto3
import os
import logging
from typing import Dict, Any, List, Optional
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from datetime import datetime

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('PROJECTS_TABLE')

if not table_name:
    logger.error("PROJECTS_TABLE environment variable not set")
    raise ValueError("PROJECTS_TABLE environment variable is required")

projects_table = dynamodb.Table(table_name)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for projects API endpoints.
    
    Supports:
    - GET /projects - List all projects
    - GET /projects/{id} - Get specific project
    - GET /projects?status={status} - Filter by status
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response
    """
    try:
        # Log the incoming request
        logger.info(f"Processing request: {json.dumps(event, default=str)}")
        
        # Check if specific project ID requested
        path_params = event.get('pathParameters') or {}
        project_id = path_params.get('id')
        
        if project_id:
            return _get_project_by_id(project_id)
        else:
            return _list_projects(event)
            
    except ClientError as e:
        logger.error(f"DynamoDB error: {e}")
        return _error_response(500, "Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return _error_response(500, "Internal server error")

def _get_project_by_id(project_id: str) -> Dict[str, Any]:
    """
    Get a specific project by ID.
    
    Args:
        project_id: Project ID to retrieve
        
    Returns:
        API Gateway response with project data
    """
    try:
        response = projects_table.get_item(
            Key={'project_id': project_id}
        )
        
        if 'Item' not in response:
            logger.warning(f"Project not found: {project_id}")
            return _error_response(404, "Project not found")
        
        project = response['Item']
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(project)
        }
        
    except ClientError as e:
        logger.error(f"Error getting project {project_id}: {e}")
        raise

def _list_projects(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    List all projects with optional filtering.
    
    Args:
        event: API Gateway event
        
    Returns:
        API Gateway response with projects list
    """
    try:
        # Parse query parameters
        query_params = event.get('queryStringParameters') or {}
        status_filter = query_params.get('status')
        
        # Scan all projects
        response = projects_table.scan()
        projects = response.get('Items', [])
        
        # Apply filters
        if status_filter:
            projects = [p for p in projects if p.get('status', '').lower() == status_filter.lower()]
        
        # Sort by start_date (newest first)
        projects.sort(key=lambda x: x.get('start_date', ''), reverse=True)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'projects': projects,
                'count': len(projects),
                'filters': {
                    'status': status_filter
                }
            })
        }
        
    except ClientError as e:
        logger.error(f"Error listing projects: {e}")
        raise

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