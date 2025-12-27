import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    try:
        # Parse the request
        http_method = event['httpMethod']
        path = event['path']
        
        # Route to appropriate handler
        if path.endswith('/admin/skills'):
            return handle_skills(event, http_method)
        elif path.endswith('/admin/certifications'):
            return handle_certifications(event, http_method)
        elif path.endswith('/admin/projects'):
            return handle_projects(event, http_method)
        elif path.endswith('/admin/adrs'):
            return handle_adrs(event, http_method)
        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Endpoint not found'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }

def handle_skills(event, method):
    table = dynamodb.Table('oyins-journey-skills')
    
    if method == 'POST':
        data = json.loads(event['body'])
        table.put_item(Item=data)
        return success_response('Skill added successfully')
    
    return method_not_allowed()

def handle_certifications(event, method):
    table = dynamodb.Table('oyins-journey-certifications')
    
    if method == 'POST':
        data = json.loads(event['body'])
        table.put_item(Item=data)
        return success_response('Certification added successfully')
    
    return method_not_allowed()

def handle_projects(event, method):
    table = dynamodb.Table('oyins-journey-projects')
    
    if method == 'POST':
        data = json.loads(event['body'])
        table.put_item(Item=data)
        return success_response('Project added successfully')
    
    return method_not_allowed()

def handle_adrs(event, method):
    table = dynamodb.Table('oyins-journey-adrs')
    
    if method == 'POST':
        data = json.loads(event['body'])
        table.put_item(Item=data)
        return success_response('ADR added successfully')
    
    return method_not_allowed()

def success_response(message):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'message': message})
    }

def method_not_allowed():
    return {
        'statusCode': 405,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'error': 'Method not allowed'})
    }