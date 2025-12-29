import json
import boto3
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('CERTIFICATIONS_TABLE')
certifications_table = dynamodb.Table(table_name)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        logger.info(f"Processing certifications request: {json.dumps(event, default=str)}")
        
        query_params = event.get('queryStringParameters') or {}
        provider = query_params.get('provider')
        status = query_params.get('status')  # active, expired, expiring_soon
        
        response = certifications_table.scan()
        certifications = response.get('Items', [])
        
        # Add status based on expiry date
        current_date = datetime.now().date()
        for cert in certifications:
            if cert.get('expiry_date'):
                expiry = datetime.strptime(cert['expiry_date'], '%Y-%m-%d').date()
                if expiry < current_date:
                    cert['computed_status'] = 'expired'
                elif expiry < current_date + timedelta(days=90):
                    cert['computed_status'] = 'expiring_soon'
                else:
                    cert['computed_status'] = 'active'
            else:
                cert['computed_status'] = 'no_expiry'
        
        # Filter by provider if specified
        if provider:
            certifications = [c for c in certifications if 
                            c.get('provider', '').lower() == provider.lower()]
        
        # Filter by status if specified
        if status:
            certifications = [c for c in certifications if 
                            c.get('computed_status') == status]
        
        # Sort by issue date (most recent first)
        certifications.sort(key=lambda x: x.get('issue_date', ''), reverse=True)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'certifications': certifications,
                'count': len(certifications),
                'filters': {'provider': provider, 'status': status}
            })
        }
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Internal server error'})
        }