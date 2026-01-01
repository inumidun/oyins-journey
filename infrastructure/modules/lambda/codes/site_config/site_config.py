import json
import boto3
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Configure logging
logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('SITE_CONFIG_TABLE', 'oyins-journey-site-config')
table = dynamodb.Table(table_name)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handle site configuration requests
    GET /config - Get site configuration
    PUT /admin/config - Update site configuration (admin only)
    """
    try:
        http_method = event.get('httpMethod', '')
        path = event.get('path', '')
        
        logger.info(f"Processing {http_method} request to {path}")
        
        if http_method == 'GET' and path == '/config':
            return get_site_config()
        elif http_method == 'PUT' and path == '/admin/config':
            return update_site_config(event)
        else:
            return {
                'statusCode': 404,
                'headers': get_cors_headers(),
                'body': json.dumps({'error': 'Endpoint not found'})
            }
            
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {
            'statusCode': 500,
            'headers': get_cors_headers(),
            'body': json.dumps({'error': 'Internal server error'})
        }

def get_site_config() -> Dict[str, Any]:
    """Get the current site configuration"""
    try:
        # Try to get existing config
        response = table.get_item(Key={'config_id': 'site-config'})
        
        if 'Item' in response:
            config = response['Item']
            # Remove DynamoDB metadata
            config.pop('config_id', None)
            config.pop('updated_at', None)
        else:
            # Return default configuration if none exists
            config = get_default_config()
        
        return {
            'statusCode': 200,
            'headers': get_cors_headers(),
            'body': json.dumps(config)
        }
        
    except Exception as e:
        logger.error(f"Error getting site config: {str(e)}")
        return {
            'statusCode': 500,
            'headers': get_cors_headers(),
            'body': json.dumps({'error': 'Failed to get site configuration'})
        }

def update_site_config(event: Dict[str, Any]) -> Dict[str, Any]:
    """Update site configuration (admin only)"""
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        # Validate required fields
        if not isinstance(body, dict):
            return {
                'statusCode': 400,
                'headers': get_cors_headers(),
                'body': json.dumps({'error': 'Invalid request body'})
            }
        
        # Validate social links if provided
        if 'socialLinks' in body:
            social_links = body['socialLinks']
            if not isinstance(social_links, dict):
                return {
                    'statusCode': 400,
                    'headers': get_cors_headers(),
                    'body': json.dumps({'error': 'socialLinks must be an object'})
                }
            
            # Validate URLs
            for key, url in social_links.items():
                if url and not is_valid_url(url):
                    return {
                        'statusCode': 400,
                        'headers': get_cors_headers(),
                        'body': json.dumps({'error': f'Invalid URL for {key}: {url}'})
                    }
        
        # Prepare config item
        config_item = {
            'config_id': 'site-config',
            'updated_at': datetime.utcnow().isoformat(),
            **body
        }
        
        # Save to DynamoDB
        table.put_item(Item=config_item)
        
        # Return updated config (without metadata)
        response_config = {k: v for k, v in config_item.items() 
                          if k not in ['config_id', 'updated_at']}
        
        return {
            'statusCode': 200,
            'headers': get_cors_headers(),
            'body': json.dumps(response_config)
        }
        
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': get_cors_headers(),
            'body': json.dumps({'error': 'Invalid JSON in request body'})
        }
    except Exception as e:
        logger.error(f"Error updating site config: {str(e)}")
        return {
            'statusCode': 500,
            'headers': get_cors_headers(),
            'body': json.dumps({'error': 'Failed to update site configuration'})
        }

def get_default_config() -> Dict[str, Any]:
    """Return default site configuration"""
    return {
        'socialLinks': {
            'linkedin': 'https://linkedin.com/in/oyindamola-oladipo',
            'github': 'https://github.com/oyindamola-oladipo',
            'email': 'mailto:hello@oyins-journey.dev'
        },
        'branding': {
            'name': 'Oyin',
            'tagline': 'Cloud Engineer & Solutions Architect'
        },
        'sourceRepoUrl': 'https://github.com/oyindamola-oladipo/oyins-journey',
        'liveApiUrl': 'https://api.oyins-journey.dev'
    }

def is_valid_url(url: str) -> bool:
    """Basic URL validation"""
    if not url:
        return True  # Empty URLs are allowed
    
    # Basic validation - starts with http/https or mailto
    return (url.startswith('http://') or 
            url.startswith('https://') or 
            url.startswith('mailto:'))

def get_cors_headers() -> Dict[str, str]:
    """Get CORS headers for responses"""
    return {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET,PUT,OPTIONS'
    }