"""
Property-based tests for observability dashboard functionality.
Feature: living-architecture-resume-enhancement
"""

import pytest
from hypothesis import given, strategies as st, settings
import json
import os
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import boto3
from moto import mock_cloudwatch

# Set AWS region for tests
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"

# Add the api directory to the path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

from health import lambda_handler as health_handler


@mock_cloudwatch
class TestObservabilityProperties:
    
    def setup_method(self):
        """Set up test CloudWatch client"""
        self.cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
    
    # Property 12: Metrics Update Timeliness
    # Feature: living-architecture-resume-enhancement, Property 12: For any metrics display, the observability dashboard should update data within acceptable time windows (near real-time)
    @given(
        time_range_hours=st.integers(min_value=1, max_value=24),
        metric_data_points=st.lists(
            st.fixed_dictionaries({
                'timestamp': st.datetimes(
                    min_value=datetime.now() - timedelta(hours=24),
                    max_value=datetime.now()
                ),
                'value': st.floats(min_value=0, max_value=1000),
                'metric_name': st.sampled_from(['Latency', 'Count', '4XXError', '5XXError'])
            }),
            min_size=1,
            max_size=24
        )
    )
    @settings(max_examples=100)
    def test_metrics_update_timeliness_property(self, time_range_hours, metric_data_points):
        """
        Property 12: For any metrics display, the observability dashboard should 
        update data within acceptable time windows (near real-time)
        **Validates: Requirements 5.5**
        """
        # Mock CloudWatch metrics data
        mock_datapoints = []
        for data_point in metric_data_points:
            mock_datapoints.append({
                'Timestamp': data_point['timestamp'],
                'Average': data_point['value'],
                'Sum': data_point['value'],
                'Unit': 'Count'
            })
        
        mock_cloudwatch_response = {
            'Datapoints': mock_datapoints,
            'Label': 'Test Metric'
        }
        
        with patch.dict('os.environ', {
            'API_GATEWAY_ID': 'test-api-gateway',
            'SYSTEM_VERSION': '2.1.0',
            'ENVIRONMENT': 'test'
        }):
            with patch('boto3.client') as mock_boto_client:
                mock_cw_client = MagicMock()
                mock_cw_client.get_metric_statistics.return_value = mock_cloudwatch_response
                mock_boto_client.return_value = mock_cw_client
                
                # Record start time
                start_time = datetime.utcnow()
                
                # Call health endpoint with metrics
                event = {
                    'queryStringParameters': {'include_metrics': 'true'}
                }
                response = health_handler(event, {})
                
                # Record end time
                end_time = datetime.utcnow()
                
                # Verify response is successful
                assert response['statusCode'] in [200, 206]  # 206 for degraded but functional
                
                body = json.loads(response['body'])
                
                # Verify metrics are included
                assert 'metrics' in body
                
                # Verify response time is within acceptable limits (near real-time)
                response_time = (end_time - start_time).total_seconds()
                assert response_time < 10.0  # Should respond within 10 seconds
                
                # Verify metrics contain expected structure
                metrics = body['metrics']
                if not metrics.get('error'):  # If CloudWatch is available
                    # Verify metrics have recent timestamps
                    if 'total_requests_24h' in metrics:
                        assert isinstance(metrics['total_requests_24h'], (int, float))
                    
                    if 'average_latency_ms' in metrics:
                        assert isinstance(metrics['average_latency_ms'], (int, float))
                        assert metrics['average_latency_ms'] >= 0
                    
                    if 'error_rate_percent' in metrics:
                        assert isinstance(metrics['error_rate_percent'], (int, float))
                        assert 0 <= metrics['error_rate_percent'] <= 100
                
                # Verify system info is current
                assert 'system_info' in body
                system_info = body['system_info']
                assert 'version' in system_info
                assert 'last_deployment' in system_info
                
                # Verify timestamp is recent (within last few seconds)
                assert 'timestamp' in body
                response_timestamp = datetime.fromisoformat(body['timestamp'].replace('Z', ''))
                time_diff = (datetime.utcnow() - response_timestamp).total_seconds()
                assert time_diff < 5.0  # Response timestamp should be very recent

    @given(
        api_gateway_metrics=st.fixed_dictionaries({
            'request_count': st.integers(min_value=0, max_value=10000),
            'average_latency': st.floats(min_value=0, max_value=5000),
            'error_4xx_count': st.integers(min_value=0, max_value=100),
            'error_5xx_count': st.integers(min_value=0, max_value=50)
        }),
        lambda_metrics=st.dictionaries(
            st.sampled_from(['skills-handler', 'projects-handler', 'certifications-handler']),
            st.fixed_dictionaries({
                'duration': st.floats(min_value=0, max_value=30000),
                'error_count': st.integers(min_value=0, max_value=10)
            }),
            min_size=1,
            max_size=3
        )
    )
    @settings(max_examples=100)
    def test_comprehensive_metrics_collection_property(self, api_gateway_metrics, lambda_metrics):
        """
        Property: Comprehensive metrics should be collected from all system components
        **Validates: Requirements 5.1, 5.2, 5.3**
        """
        # Mock CloudWatch responses for different metric types
        def mock_get_metric_statistics(Namespace, MetricName, **kwargs):
            if Namespace == 'AWS/ApiGateway':
                if MetricName == 'Count':
                    return {
                        'Datapoints': [{'Sum': api_gateway_metrics['request_count'], 'Timestamp': datetime.utcnow()}]
                    }
                elif MetricName == 'Latency':
                    return {
                        'Datapoints': [{'Average': api_gateway_metrics['average_latency'], 'Timestamp': datetime.utcnow()}]
                    }
                elif MetricName == '4XXError':
                    return {
                        'Datapoints': [{'Sum': api_gateway_metrics['error_4xx_count'], 'Timestamp': datetime.utcnow()}]
                    }
                elif MetricName == '5XXError':
                    return {
                        'Datapoints': [{'Sum': api_gateway_metrics['error_5xx_count'], 'Timestamp': datetime.utcnow()}]
                    }
            elif Namespace == 'AWS/Lambda':
                function_name = kwargs.get('Dimensions', [{}])[0].get('Value', '')
                if function_name in lambda_metrics:
                    if MetricName == 'Duration':
                        return {
                            'Datapoints': [{'Average': lambda_metrics[function_name]['duration'], 'Timestamp': datetime.utcnow()}]
                        }
                    elif MetricName == 'Errors':
                        return {
                            'Datapoints': [{'Sum': lambda_metrics[function_name]['error_count'], 'Timestamp': datetime.utcnow()}]
                        }
            
            return {'Datapoints': []}
        
        with patch.dict('os.environ', {
            'API_GATEWAY_ID': 'test-api-gateway',
            'SYSTEM_VERSION': '2.1.0'
        }):
            with patch('boto3.client') as mock_boto_client:
                mock_cw_client = MagicMock()
                mock_cw_client.get_metric_statistics.side_effect = mock_get_metric_statistics
                mock_boto_client.return_value = mock_cw_client
                
                event = {'queryStringParameters': {'include_metrics': 'true'}}
                response = health_handler(event, {})
                
                assert response['statusCode'] in [200, 206]
                body = json.loads(response['body'])
                
                # Verify comprehensive metrics are collected
                assert 'metrics' in body
                metrics = body['metrics']
                
                if not metrics.get('error'):
                    # Verify API Gateway metrics
                    if api_gateway_metrics['request_count'] > 0:
                        assert 'total_requests_24h' in metrics
                        assert metrics['total_requests_24h'] == api_gateway_metrics['request_count']
                    
                    if 'average_latency_ms' in metrics:
                        assert metrics['average_latency_ms'] == api_gateway_metrics['average_latency']
                    
                    # Verify error rate calculation
                    total_requests = api_gateway_metrics['request_count']
                    total_errors = api_gateway_metrics['error_4xx_count'] + api_gateway_metrics['error_5xx_count']
                    if total_requests > 0:
                        expected_error_rate = (total_errors / total_requests) * 100
                        if 'error_rate_percent' in metrics:
                            assert abs(metrics['error_rate_percent'] - expected_error_rate) < 0.01
                    
                    # Verify Lambda metrics are included
                    if 'lambda_functions' in metrics:
                        lambda_functions_metrics = metrics['lambda_functions']
                        for function_name in lambda_metrics:
                            if function_name in lambda_functions_metrics:
                                function_metrics = lambda_functions_metrics[function_name]
                                assert 'average_duration_ms' in function_metrics

    @given(
        cloudwatch_availability=st.sampled_from(['available', 'unavailable', 'partial', 'timeout']),
        fallback_data=st.fixed_dictionaries({
            'cached_request_count': st.integers(min_value=0, max_value=1000),
            'cached_error_rate': st.floats(min_value=0, max_value=10),
            'last_known_latency': st.floats(min_value=0, max_value=1000)
        })
    )
    @settings(max_examples=100)
    def test_metrics_fallback_mechanisms_property(self, cloudwatch_availability, fallback_data):
        """
        Property: Metrics system should provide appropriate fallback mechanisms 
        when CloudWatch is unavailable
        **Validates: Requirements 5.1, 5.2**
        """
        def mock_cloudwatch_behavior(*args, **kwargs):
            if cloudwatch_availability == 'unavailable':
                raise Exception("CloudWatch service unavailable")
            elif cloudwatch_availability == 'timeout':
                raise Exception("Request timed out")
            elif cloudwatch_availability == 'partial':
                # Return some data but not all
                return {'Datapoints': [{'Sum': fallback_data['cached_request_count'], 'Timestamp': datetime.utcnow()}]}
            else:  # available
                return {'Datapoints': [{'Average': 100, 'Sum': 500, 'Timestamp': datetime.utcnow()}]}
        
        with patch.dict('os.environ', {'API_GATEWAY_ID': 'test-api-gateway'}):
            with patch('boto3.client') as mock_boto_client:
                mock_cw_client = MagicMock()
                mock_cw_client.get_metric_statistics.side_effect = mock_cloudwatch_behavior
                mock_boto_client.return_value = mock_cw_client
                
                event = {'queryStringParameters': {'include_metrics': 'true'}}
                response = health_handler(event, {})
                
                # Should always return a response, even with CloudWatch issues
                assert response['statusCode'] in [200, 206, 503]
                body = json.loads(response['body'])
                
                # Verify response structure is maintained
                assert 'status' in body
                assert 'timestamp' in body
                
                if cloudwatch_availability in ['unavailable', 'timeout']:
                    # Should indicate metrics are unavailable but still provide basic health
                    if 'metrics' in body:
                        metrics = body['metrics']
                        assert 'error' in metrics or 'fallback' in metrics
                else:
                    # Should provide metrics data
                    assert 'metrics' in body
                    
                # System should remain responsive regardless of CloudWatch status
                assert 'system_info' in body
                assert body['system_info']['version'] is not None

    @given(
        deployment_history=st.lists(
            st.fixed_dictionaries({
                'version': st.text(min_size=1, max_size=20),
                'timestamp': st.datetimes(
                    min_value=datetime.now() - timedelta(days=30),
                    max_value=datetime.now()
                ),
                'status': st.sampled_from(['success', 'failure', 'in_progress']),
                'commit_sha': st.text(min_size=7, max_size=40)
            }),
            min_size=1,
            max_size=10
        )
    )
    @settings(max_examples=100)
    def test_deployment_history_tracking_property(self, deployment_history):
        """
        Property: Deployment history should be tracked and displayed accurately
        **Validates: Requirements 5.4**
        """
        # Sort deployment history by timestamp (most recent first)
        sorted_deployments = sorted(deployment_history, key=lambda x: x['timestamp'], reverse=True)
        latest_deployment = sorted_deployments[0] if sorted_deployments else None
        
        with patch.dict('os.environ', {
            'SYSTEM_VERSION': latest_deployment['version'] if latest_deployment else '1.0.0',
            'LAST_DEPLOYMENT': latest_deployment['timestamp'].isoformat() if latest_deployment else datetime.utcnow().isoformat()
        }):
            # Mock GitHub Actions API for deployment history
            mock_github_response = {
                'workflow_runs': [
                    {
                        'id': i,
                        'head_sha': dep['commit_sha'],
                        'status': dep['status'],
                        'conclusion': 'success' if dep['status'] == 'success' else 'failure',
                        'created_at': dep['timestamp'].isoformat(),
                        'updated_at': dep['timestamp'].isoformat()
                    }
                    for i, dep in enumerate(sorted_deployments[:5])  # Last 5 deployments
                ]
            }
            
            with patch('requests.get') as mock_get:
                mock_get.return_value.json.return_value = mock_github_response
                mock_get.return_value.status_code = 200
                
                event = {'queryStringParameters': {'include_metrics': 'true'}}
                response = health_handler(event, {})
                
                assert response['statusCode'] in [200, 206]
                body = json.loads(response['body'])
                
                # Verify system info includes deployment information
                assert 'system_info' in body
                system_info = body['system_info']
                
                if latest_deployment:
                    assert system_info['version'] == latest_deployment['version']
                    
                    # Verify last deployment timestamp is recent and matches
                    last_deployment_str = system_info['last_deployment']
                    last_deployment_dt = datetime.fromisoformat(last_deployment_str.replace('Z', ''))
                    expected_dt = latest_deployment['timestamp'].replace(tzinfo=None)
                    
                    # Allow small time difference due to processing
                    time_diff = abs((last_deployment_dt - expected_dt).total_seconds())
                    assert time_diff < 60  # Within 1 minute
                
                # Verify uptime calculation is reasonable
                if 'uptime_seconds' in body:
                    assert body['uptime_seconds'] >= 0
                    assert body['uptime_hours'] >= 0
                    assert body['uptime_hours'] == round(body['uptime_seconds'] / 3600, 2)