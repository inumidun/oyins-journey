import json
import boto3
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
# Use environment variable for table name (no hardcoded environment)
table_name = os.environ.get('PROJECTS_TABLE', 'oyins-journey-projects')
projects_table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Check if specific project ID requested
        path_params = event.get('pathParameters') or {}
        project_id = path_params.get('id')
        
        if project_id:
            # Get specific project
            response = projects_table.get_item(
                Key={'project_id': project_id}
            )
            
            if 'Item' not in response:
                return {
                    'statusCode': 404,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'error': 'Project not found'
                    })
                }
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(response['Item'])
            }
        else:
            # Get all projects
            response = projects_table.scan()
            projects = response['Items']
            
            # Sort by date (newest first)
            projects.sort(key=lambda x: x.get('start_date', ''), reverse=True)
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'projects': projects,
                    'count': len(projects)
                })
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }