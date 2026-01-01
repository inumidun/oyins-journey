import json
import boto3
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('CERTIFICATIONS_TABLE')
certifications_table = dynamodb.Table(table_name)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        logger.info(f"Processing certifications request: {json.dumps(event, default=str)}")
        
        http_method = event.get('httpMethod', 'GET')
        
        if http_method == 'GET':
            return handle_get_certifications(event)
        elif http_method == 'POST':
            return handle_create_certification(event)
        else:
            return {
                'statusCode': 405,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Method not allowed'})
            }
            
    except ClientError as e:
        logger.error(f"DynamoDB error: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Database error occurred'})
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Internal server error'})
        }

def handle_get_certifications(event: Dict[str, Any]) -> Dict[str, Any]:
    query_params = event.get('queryStringParameters') or {}
    provider = query_params.get('provider')  # AWS, Azure, GCP, Other
    category = query_params.get('category')  # cloud, security, devops, data
    status = query_params.get('status')      # active, expired, expiring_soon
    include_expired = query_params.get('includeExpired', 'true').lower() == 'true'
    
    # Use GSI for efficient querying when possible
    if provider:
        # Query by provider using GSI
        response = certifications_table.query(
            IndexName='ProviderIndex',
            KeyConditionExpression=Key('provider').eq(provider)
        )
        certifications = response.get('Items', [])
    elif category:
        # Query by category using GSI
        response = certifications_table.query(
            IndexName='CategoryIndex',
            KeyConditionExpression=Key('category').eq(category)
        )
        certifications = response.get('Items', [])
    else:
        # Scan all certifications
        response = certifications_table.scan()
        certifications = response.get('Items', [])
    
    # Add computed status based on expiry date
    current_date = datetime.now().date()
    for cert in certifications:
        # Calculate expiry status
        if cert.get('expiry_date'):
            try:
                expiry = datetime.strptime(cert['expiry_date'], '%Y-%m-%d').date()
                if expiry < current_date:
                    cert['computed_status'] = 'expired'
                    cert['is_expired'] = True
                    cert['renewal_required'] = True
                elif expiry < current_date + timedelta(days=90):
                    cert['computed_status'] = 'expiring_soon'
                    cert['is_expired'] = False
                    cert['renewal_required'] = True
                else:
                    cert['computed_status'] = 'active'
                    cert['is_expired'] = False
                    cert['renewal_required'] = False
            except ValueError:
                logger.warning(f"Invalid expiry date format for cert {cert.get('cert_id')}: {cert.get('expiry_date')}")
                cert['computed_status'] = 'unknown'
                cert['is_expired'] = False
                cert['renewal_required'] = False
        else:
            cert['computed_status'] = 'no_expiry'
            cert['is_expired'] = False
            cert['renewal_required'] = False
    
    # Apply additional filters
    if category and not provider:
        # Category filter already applied via GSI
        pass
    elif category and provider:
        # Both filters - category filter on top of provider GSI results
        certifications = [c for c in certifications if 
                        c.get('category', '').lower() == category.lower()]
    
    # Filter by status if specified
    if status:
        certifications = [c for c in certifications if 
                        c.get('computed_status') == status]
    
    # Filter out expired certifications unless explicitly requested
    if not include_expired:
        certifications = [c for c in certifications if not c.get('is_expired', False)]
    
    # Sort by issue date (most recent first)
    certifications.sort(key=lambda x: x.get('issue_date', ''), reverse=True)
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET, OPTIONS'
        },
        'body': json.dumps({
            'certifications': certifications,
            'count': len(certifications),
            'filters': {
                'provider': provider,
                'category': category,
                'status': status,
                'includeExpired': include_expired
            },
            'metadata': {
                'total_active': len([c for c in certifications if c.get('computed_status') == 'active']),
                'total_expired': len([c for c in certifications if c.get('computed_status') == 'expired']),
                'total_expiring_soon': len([c for c in certifications if c.get('computed_status') == 'expiring_soon'])
            }
        })
    }

def handle_create_certification(event: Dict[str, Any]) -> Dict[str, Any]:
    # Parse request body
    try:
        body = json.loads(event.get('body', '{}'))
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Invalid JSON in request body'})
        }
    
    # Validate required fields
    required_fields = ['name', 'provider', 'earned_date']
    for field in required_fields:
        if not body.get(field):
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': f'Missing required field: {field}'})
            }
    
    # Create certification item
    import uuid
    cert_id = body.get('cert_id') or f"cert-{uuid.uuid4().hex[:8]}"
    
    cert_item = {
        'cert_id': cert_id,
        'name': body['name'],
        'provider': body['provider'],
        'earned_date': body['earned_date'],
        'expiry_date': body.get('expiry_date'),
        'status': body.get('status', 'active'),
        'credential_id': body.get('credential_id', ''),
        'verification_url': body.get('verification_url', ''),
        'skills_demonstrated': body.get('skills_demonstrated', []),
        'category': body.get('category', 'cloud'),
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    # Save to DynamoDB
    try:
        certifications_table.put_item(Item=cert_item)
        
        return {
            'statusCode': 201,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Certification created successfully',
                'certification': cert_item
            })
        }
        
    except Exception as e:
        logger.error(f"Error creating certification: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Failed to create certification',
                'message': str(e) if os.environ.get('DEBUG') else 'Database error'
            })
        }