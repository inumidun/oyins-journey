import json
import boto3

dynamodb = boto3.resource('dynamodb')
adrs_table = dynamodb.Table('oyins-journey-adrs')

def lambda_handler(event, context):
    try:
        response = adrs_table.scan()
        adrs = response['Items']
        
        # Sort by decision date (newest first)
        adrs.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'decisions': adrs,
                'count': len(adrs)
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