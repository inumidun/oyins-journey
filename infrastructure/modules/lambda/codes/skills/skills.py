import json
import boto3
import os
import logging
from typing import Dict, Any, List, Optional
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('SKILLS_TABLE')

if not table_name:
    logger.error("SKILLS_TABLE environment variable not set")
    raise ValueError("SKILLS_TABLE environment variable is required")

skills_table = dynamodb.Table(table_name)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for skills API endpoints.
    
    Supports:
    - GET /skills - List all skills
    - GET /skills?category={category} - Filter by category
    - GET /skills?cloud={cloud} - Filter by cloud provider
    
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
        category = query_params.get('category')
        cloud = query_params.get('cloud')
        
        # Query or scan based on parameters
        if category:
            skills = _query_by_category(category)
        else:
            skills = _scan_all_skills()
        
        # Filter by cloud if specified
        if cloud:
            skills = _filter_by_cloud(skills, cloud)
        
        # Sort skills by usage_count (most used first)
        skills.sort(key=lambda x: x.get('usage_count', 0), reverse=True)
        
        response = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'skills': skills,
                'count': len(skills),
                'filters': {
                    'category': category,
                    'cloud': cloud
                }
            })
        }
        
        logger.info(f"Returning {len(skills)} skills")
        return response
        
    except ClientError as e:
        logger.error(f"DynamoDB error: {e}")
        return _error_response(500, "Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return _error_response(500, "Internal server error")

def _query_by_category(category: str) -> List[Dict[str, Any]]:
    """
    Query skills by category using GSI.
    
    Args:
        category: Skill category to filter by
        
    Returns:
        List of skills in the category
    """
    try:
        response = skills_table.query(
            IndexName='CategoryIndex',
            KeyConditionExpression=Key('category').eq(category.lower())
        )
        return response.get('Items', [])
    except ClientError as e:
        logger.error(f"Error querying by category {category}: {e}")
        raise

def _scan_all_skills() -> List[Dict[str, Any]]:
    """
    Scan all skills from the table.
    
    Returns:
        List of all skills
    """
    try:
        response = skills_table.scan()
        return response.get('Items', [])
    except ClientError as e:
        logger.error(f"Error scanning skills table: {e}")
        raise

def _filter_by_cloud(skills: List[Dict[str, Any]], cloud: str) -> List[Dict[str, Any]]:
    """
    Filter skills by cloud provider.
    
    Args:
        skills: List of skills to filter
        cloud: Cloud provider to filter by
        
    Returns:
        Filtered list of skills
    """
    cloud_lower = cloud.lower()
    filtered_skills = []
    
    for skill in skills:
        technologies = skill.get('technologies', [])
        if isinstance(technologies, list):
            # Check if any technology contains the cloud provider
            if any(cloud_lower in tech.lower() for tech in technologies):
                filtered_skills.append(skill)
        elif isinstance(technologies, str):
            # Handle case where technologies is a string
            if cloud_lower in technologies.lower():
                filtered_skills.append(skill)
    
    return filtered_skills

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