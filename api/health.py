import json
import boto3
import os
from datetime import datetime, timedelta

# Initialize AWS clients
cloudwatch = boto3.client('cloudwatch')
dynamodb = boto3.resource('dynamodb')

def get_cloudwatch_metrics():
    """
    Fetch real CloudWatch metrics for the system
    """
    try:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=24)
        
        metrics = {}
        
        # Get API Gateway metrics
        api_gateway_id = os.environ.get('API_GATEWAY_ID')
        if api_gateway_id:
            # Request count
            response = cloudwatch.get_metric_statistics(
                Namespace='AWS/ApiGateway',
                MetricName='Count',
                Dimensions=[
                    {'Name': 'ApiName', 'Value': api_gateway_id}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,  # 1 hour
                Statistics=['Sum']
            )
            
            total_requests = sum([point['Sum'] for point in response['Datapoints']])
            metrics['total_requests_24h'] = int(total_requests)
            
            # Latency
            response = cloudwatch.get_metric_statistics(
                Namespace='AWS/ApiGateway',
                MetricName='Latency',
                Dimensions=[
                    {'Name': 'ApiName', 'Value': api_gateway_id}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=['Average']
            )
            
            if response['Datapoints']:
                avg_latency = sum([point['Average'] for point in response['Datapoints']]) / len(response['Datapoints'])
                metrics['average_latency_ms'] = round(avg_latency, 2)
            else:
                metrics['average_latency_ms'] = 0
            
            # Error rate
            response = cloudwatch.get_metric_statistics(
                Namespace='AWS/ApiGateway',
                MetricName='4XXError',
                Dimensions=[
                    {'Name': 'ApiName', 'Value': api_gateway_id}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=['Sum']
            )
            
            client_errors = sum([point['Sum'] for point in response['Datapoints']])
            
            response = cloudwatch.get_metric_statistics(
                Namespace='AWS/ApiGateway',
                MetricName='5XXError',
                Dimensions=[
                    {'Name': 'ApiName', 'Value': api_gateway_id}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=['Sum']
            )
            
            server_errors = sum([point['Sum'] for point in response['Datapoints']])
            total_errors = client_errors + server_errors
            
            if total_requests > 0:
                metrics['error_rate_percent'] = round((total_errors / total_requests) * 100, 2)
            else:
                metrics['error_rate_percent'] = 0
        
        # Get Lambda metrics
        lambda_functions = [
            'skills-handler',
            'projects-handler',
            'certifications-handler',
            'adrs-handler'
        ]
        
        lambda_metrics = {}
        for function_name in lambda_functions:
            try:
                response = cloudwatch.get_metric_statistics(
                    Namespace='AWS/Lambda',
                    MetricName='Duration',
                    Dimensions=[
                        {'Name': 'FunctionName', 'Value': function_name}
                    ],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=3600,
                    Statistics=['Average']
                )
                
                if response['Datapoints']:
                    avg_duration = sum([point['Average'] for point in response['Datapoints']]) / len(response['Datapoints'])
                    lambda_metrics[function_name] = {
                        'average_duration_ms': round(avg_duration, 2)
                    }
            except Exception as e:
                print(f"Error getting metrics for {function_name}: {str(e)}")
                lambda_metrics[function_name] = {
                    'average_duration_ms': 0,
                    'error': 'Metrics unavailable'
                }
        
        metrics['lambda_functions'] = lambda_metrics
        
        return metrics
        
    except Exception as e:
        print(f"Error fetching CloudWatch metrics: {str(e)}")
        return {
            'error': 'CloudWatch metrics unavailable',
            'fallback': True
        }

def get_system_health():
    """
    Check system health by testing DynamoDB connectivity
    """
    health_status = {
        'status': 'healthy',
        'checks': {},
        'timestamp': datetime.utcnow().isoformat()
    }
    
    # Test DynamoDB connectivity
    try:
        # Test skills table
        skills_table_name = os.environ.get('SKILLS_TABLE', 'oyins-journey-skills')
        skills_table = dynamodb.Table(skills_table_name)
        skills_table.table_status
        health_status['checks']['skills_database'] = 'healthy'
    except Exception as e:
        health_status['checks']['skills_database'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'degraded'
    
    try:
        # Test projects table
        projects_table_name = os.environ.get('PROJECTS_TABLE', 'oyins-journey-projects')
        projects_table = dynamodb.Table(projects_table_name)
        projects_table.table_status
        health_status['checks']['projects_database'] = 'healthy'
    except Exception as e:
        health_status['checks']['projects_database'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'degraded'
    
    try:
        # Test certifications table
        certifications_table_name = os.environ.get('CERTIFICATIONS_TABLE', 'oyins-journey-certifications')
        certifications_table = dynamodb.Table(certifications_table_name)
        certifications_table.table_status
        health_status['checks']['certifications_database'] = 'healthy'
    except Exception as e:
        health_status['checks']['certifications_database'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'degraded'
    
    return health_status

def lambda_handler(event, context):
    try:
        # Parse query parameters
        query_params = event.get('queryStringParameters') or {}
        include_metrics = query_params.get('include_metrics', 'true').lower() == 'true'
        
        # Get basic system health
        health_data = get_system_health()
        
        # Add CloudWatch metrics if requested
        if include_metrics:
            metrics = get_cloudwatch_metrics()
            health_data['metrics'] = metrics
        
        # Add system information
        health_data['system_info'] = {
            'version': os.environ.get('SYSTEM_VERSION', '2.1.0'),
            'environment': os.environ.get('ENVIRONMENT', 'production'),
            'region': os.environ.get('AWS_REGION', 'us-east-1'),
            'last_deployment': os.environ.get('LAST_DEPLOYMENT', datetime.utcnow().isoformat())
        }
        
        # Add uptime calculation
        deployment_time = health_data['system_info']['last_deployment']
        try:
            deploy_dt = datetime.fromisoformat(deployment_time.replace('Z', '+00:00'))
            uptime_seconds = (datetime.utcnow() - deploy_dt.replace(tzinfo=None)).total_seconds()
            health_data['uptime_seconds'] = int(uptime_seconds)
            health_data['uptime_hours'] = round(uptime_seconds / 3600, 2)
        except Exception:
            health_data['uptime_seconds'] = 0
            health_data['uptime_hours'] = 0
        
        # Determine overall status code
        status_code = 200
        if health_data['status'] == 'degraded':
            status_code = 206  # Partial Content
        elif health_data['status'] == 'unhealthy':
            status_code = 503  # Service Unavailable
        
        return {
            'statusCode': status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(health_data)
        }
        
    except Exception as e:
        print(f"Error in health handler: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'status': 'unhealthy',
                'error': 'Health check failed',
                'message': str(e) if os.environ.get('DEBUG') else 'An error occurred',
                'timestamp': datetime.utcnow().isoformat()
            })
        }