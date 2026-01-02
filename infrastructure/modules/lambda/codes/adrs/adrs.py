import json
import boto3
import os
from datetime import datetime
import uuid

dynamodb = boto3.resource('dynamodb')
# Use environment variable for table name
table_name = os.environ.get('ADRS_TABLE', 'oyins-journey-adrs')
adrs_table = dynamodb.Table(table_name)

def get_cors_headers():
    """Get comprehensive CORS headers"""
    return {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
        'Access-Control-Max-Age': '86400'
    }

def lambda_handler(event, context):
    try:
        http_method = event.get('httpMethod', 'GET')
        
        # Handle OPTIONS requests for CORS preflight
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': get_cors_headers(),
                'body': ''
            }
        
        if http_method == 'GET':
            return handle_get_adrs(event)
        elif http_method == 'POST':
            return handle_create_adr(event)
        else:
            return {
                'statusCode': 405,
                'headers': get_cors_headers(),
                'body': json.dumps({'error': 'Method not allowed'})
            }
            
    except Exception as e:
        print(f"Error in ADRs handler: {str(e)}")
        return {
            'statusCode': 500,
            'headers': get_cors_headers(),
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e) if os.environ.get('DEBUG') else 'An error occurred'
            })
        }

def handle_get_adrs(event):
    response = adrs_table.scan()
    adrs = response['Items']
    
    # Sort by decision date (newest first)
    adrs.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    return {
        'statusCode': 200,
        'headers': get_cors_headers(),
        'body': json.dumps({
            'decisions': adrs,
            'count': len(adrs)
        })
    }

def handle_create_adr(event):
    # Parse request body
    try:
        body = json.loads(event.get('body', '{}'))
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': get_cors_headers(),
            'body': json.dumps({'error': 'Invalid JSON in request body'})
        }
    
    # Validate required fields
    required_fields = ['title', 'decision', 'context', 'decision_rationale']
    for field in required_fields:
        if not body.get(field):
            return {
                'statusCode': 400,
                'headers': get_cors_headers(),
                'body': json.dumps({'error': f'Missing required field: {field}'})
            }
    
    # Create ADR item
    adr_id = body.get('adr_id') or f"adr-{uuid.uuid4().hex[:8]}"
    
    adr_item = {
        'adr_id': adr_id,
        'title': body['title'],
        'decision': body['decision'],
        'context': body['context'],
        'options_considered': body.get('options_considered', []),
        'decision_rationale': body['decision_rationale'],
        'tradeoffs': body.get('tradeoffs', []),
        'aws_services': body.get('aws_services', []),
        'date': body.get('date', datetime.now().strftime('%Y-%m-%d')),
        'status': body.get('status', 'accepted'),
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    # Save to DynamoDB
    try:
        adrs_table.put_item(Item=adr_item)
        
        return {
            'statusCode': 201,
            'headers': get_cors_headers(),
            'body': json.dumps({
                'message': 'ADR created successfully',
                'adr': adr_item
            })
        }
        
    except Exception as e:
        print(f"Error creating ADR: {str(e)}")
        return {
            'statusCode': 500,
            'headers': get_cors_headers(),
            'body': json.dumps({
                'error': 'Failed to create ADR',
                'message': str(e) if os.environ.get('DEBUG') else 'Database error'
            })
        }