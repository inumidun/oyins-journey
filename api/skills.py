import json
import boto3
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
# Use environment variable for table name (no hardcoded environment)
table_name = os.environ.get('SKILLS_TABLE', 'oyins-journey-skills')
skills_table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Parse query parameters
        query_params = event.get('queryStringParameters') or {}
        category = query_params.get('category')
        cloud = query_params.get('cloud')
        
        if category:
            # Query by category using GSI
            response = skills_table.query(
                IndexName='CategoryIndex',
                KeyConditionExpression=Key('category').eq(category)
            )
        else:
            # Scan all skills
            response = skills_table.scan()
        
        skills = response['Items']
        
        # Filter by cloud if specified
        if cloud:
            skills = [skill for skill in skills if cloud.lower() in skill.get('technologies', []).lower()]
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'skills': skills,
                'count': len(skills)
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