import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
versions_table = dynamodb.Table('oyins-journey-versions')

def lambda_handler(event, context):
    try:
        # Get latest version
        response = versions_table.scan()
        versions = response['Items']
        
        if not versions:
            # Return default version if none exists
            current_version = {
                'version': '1.0.0',
                'release_date': datetime.now().isoformat(),
                'features': ['Initial release'],
                'deployment_count': 1
            }
        else:
            # Sort by version and get latest
            versions.sort(key=lambda x: x.get('version', ''), reverse=True)
            current_version = versions[0]
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'current_version': current_version,
                'all_versions': versions
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