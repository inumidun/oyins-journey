import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
certifications_table = dynamodb.Table('oyins-journey-certifications')

def lambda_handler(event, context):
    try:
        # Parse query parameters
        query_params = event.get('queryStringParameters') or {}
        provider = query_params.get('provider')
        status = query_params.get('status')
        
        if provider:
            # Query by provider using GSI
            response = certifications_table.query(
                IndexName='ProviderIndex',
                KeyConditionExpression=Key('provider').eq(provider)
            )
        else:
            # Scan all certifications
            response = certifications_table.scan()
        
        certifications = response['Items']
        
        # Filter by status if specified
        if status:
            certifications = [cert for cert in certifications if cert.get('status', '').lower() == status.lower()]
        
        # Sort by earned date (newest first)
        certifications.sort(key=lambda x: x.get('earned_date', ''), reverse=True)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'certifications': certifications,
                'count': len(certifications)
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