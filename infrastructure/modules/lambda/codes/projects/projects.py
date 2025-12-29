import json
import boto3
import os
import logging
from typing import Dict, Any, List
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('PROJECTS_TABLE')
projects_table = dynamodb.Table(table_name)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        logger.info(f"Processing projects request: {json.dumps(event, default=str)}")
        
        query_params = event.get('queryStringParameters') or {}
        technology = query_params.get('technology')
        status = query_params.get('status')
        
        response = projects_table.scan()
        projects = response.get('Items', [])
        
        # Filter by technology if specified
        if technology:
            projects = [p for p in projects if technology.lower() in 
                       [tech.lower() for tech in p.get('technologies', [])]]
        
        # Filter by status if specified
        if status:
            projects = [p for p in projects if p.get('status', '').lower() == status.lower()]
        
        # Sort by date (most recent first)
        projects.sort(key=lambda x: x.get('end_date', x.get('start_date', '')), reverse=True)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'projects': projects,
                'count': len(projects),
                'filters': {'technology': technology, 'status': status}
            })
        }
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Internal server error'})
        }