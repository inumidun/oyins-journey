"""
Integration tests for complete user flows in the Living Architecture Resume system.
Tests end-to-end functionality across all components.
"""

import pytest
import requests
import json
import time
import os
from datetime import datetime
from unittest.mock import patch, MagicMock
import boto3
from moto.dynamodb import mock_dynamodb

# Set AWS region for tests
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"


class TestIntegrationFlows:
    """Integration tests for complete user flows"""
    
    @pytest.fixture
    def api_base_url(self):
        """Base URL for API testing"""
        return "https://api.oyins-journey.dev"  # Update with actual API URL
    
    @pytest.fixture
    def frontend_url(self):
        """Frontend URL for UI testing"""
        return "https://oyins-journey.dev"  # Update with actual frontend URL
    
    def test_complete_certification_browsing_flow(self, api_base_url):
        """
        Test end-to-end certification browsing and filtering
        **Requirements: 1.1, 1.2, 1.3, 1.4**
        """
        # Step 1: Get all certifications
        response = requests.get(f"{api_base_url}/certifications")
        assert response.status_code == 200
        
        all_certs = response.json()
        assert 'certifications' in all_certs
        assert len(all_certs['certifications']) > 0
        
        # Step 2: Filter by provider (AWS)
        response = requests.get(f"{api_base_url}/certifications?provider=AWS")
        assert response.status_code == 200
        
        aws_certs = response.json()
        assert 'certifications' in aws_certs
        
        # Verify all returned certifications are from AWS
        for cert in aws_certs['certifications']:
            assert cert['provider'] == 'AWS'
        
        # Step 3: Filter by status (active)
        response = requests.get(f"{api_base_url}/certifications?status=active")
        assert response.status_code == 200
        
        active_certs = response.json()
        assert 'certifications' in active_certs
        
        # Verify all returned certifications are active
        for cert in active_certs['certifications']:
            assert cert['computed_status'] == 'active'
        
        # Step 4: Combined filtering
        response = requests.get(f"{api_base_url}/certifications?provider=AWS&status=active")
        assert response.status_code == 200
        
        filtered_certs = response.json()
        assert 'certifications' in filtered_certs
        
        # Verify combined filters work
        for cert in filtered_certs['certifications']:
            assert cert['provider'] == 'AWS'
            assert cert['computed_status'] == 'active'
        
        # Step 5: Verify metadata is included
        if filtered_certs['certifications']:
            cert = filtered_certs['certifications'][0]
            required_fields = ['id', 'name', 'provider', 'issue_date', 'computed_status']
            for field in required_fields:
                assert field in cert
    
    def test_api_explorer_with_all_endpoints(self, api_base_url):
        """
        Test API Explorer with all endpoints
        **Requirements: 2.1, 2.2, 2.3, 2.4, 2.5**
        """
        endpoints_to_test = [
            '/skills',
            '/projects',
            '/certifications',
            '/adrs',
            '/health'
        ]
        
        for endpoint in endpoints_to_test:
            # Test basic endpoint access
            response = requests.get(f"{api_base_url}{endpoint}")
            assert response.status_code in [200, 206]  # 206 for degraded health
            
            # Verify response is JSON
            try:
                data = response.json()
                assert isinstance(data, dict)
            except json.JSONDecodeError:
                pytest.fail(f"Endpoint {endpoint} did not return valid JSON")
            
            # Test with query parameters where applicable
            if endpoint in ['/skills', '/projects', '/certifications']:
                # Test with limit parameter
                response = requests.get(f"{api_base_url}{endpoint}?limit=5")
                assert response.status_code == 200
                
                # Test error handling with invalid parameters
                response = requests.get(f"{api_base_url}{endpoint}?invalid_param=test")
                # Should still work, just ignore invalid params
                assert response.status_code == 200
        
        # Test health endpoint with metrics
        response = requests.get(f"{api_base_url}/health?include_metrics=true")
        assert response.status_code in [200, 206]
        
        health_data = response.json()
        assert 'status' in health_data
        assert 'timestamp' in health_data
        
        # If metrics are available, verify structure
        if 'metrics' in health_data and not health_data['metrics'].get('error'):
            metrics = health_data['metrics']
            # Should have some metric data
            assert isinstance(metrics, dict)
    
    def test_evidence_link_validation_flow(self, api_base_url):
        """
        Test evidence link validation flows
        **Requirements: 4.1, 4.2, 4.3, 4.4, 4.5**
        """
        # Step 1: Get projects with evidence links
        response = requests.get(f"{api_base_url}/projects?include_github=true")
        assert response.status_code == 200
        
        projects = response.json()
        assert 'projects' in projects
        
        # Find a project with evidence links or GitHub URL
        project_with_evidence = None
        for project in projects['projects']:
            if project.get('evidence_links') or project.get('github_url'):
                project_with_evidence = project
                break
        
        if project_with_evidence:
            # Step 2: Verify evidence links are validated
            if 'evidence_links' in project_with_evidence:
                for link in project_with_evidence['evidence_links']:
                    assert 'status' in link
                    assert link['status'] in ['active', 'inactive', 'error', 'timeout']
                    assert 'last_checked' in link
            
            # Step 3: Verify GitHub enrichment
            if 'github_url' in project_with_evidence and 'github_stats' in project_with_evidence:
                github_stats = project_with_evidence['github_stats']
                expected_fields = ['stars', 'forks', 'commits_last_30_days']
                for field in expected_fields:
                    assert field in github_stats
        
        # Step 4: Get skills with evidence
        response = requests.get(f"{api_base_url}/skills")
        assert response.status_code == 200
        
        skills = response.json()
        assert 'skills' in skills
        
        # Verify skills have evidence linking capability
        for skill in skills['skills'][:3]:  # Check first 3 skills
            # Should have evidence summary or links
            if 'evidence_links' in skill:
                for link in skill['evidence_links']:
                    assert 'type' in link
                    assert link['type'] in ['repository', 'documentation', 'demo']
    
    def test_real_time_metrics_and_observability(self, api_base_url):
        """
        Test real-time metrics and observability features
        **Requirements: 5.1, 5.2, 5.3, 5.4, 5.5**
        """
        # Step 1: Get health status
        response = requests.get(f"{api_base_url}/health")
        assert response.status_code in [200, 206, 503]  # Various health states
        
        health_data = response.json()
        assert 'status' in health_data
        assert 'timestamp' in health_data
        
        # Verify timestamp is recent (within last minute)
        timestamp = datetime.fromisoformat(health_data['timestamp'].replace('Z', ''))
        time_diff = (datetime.utcnow() - timestamp).total_seconds()
        assert time_diff < 60  # Within 1 minute
        
        # Step 2: Get detailed metrics
        response = requests.get(f"{api_base_url}/health?include_metrics=true")
        assert response.status_code in [200, 206, 503]
        
        detailed_health = response.json()
        
        # Verify system info is present
        if 'system_info' in detailed_health:
            system_info = detailed_health['system_info']
            assert 'version' in system_info
            assert 'environment' in system_info
        
        # Step 3: Test multiple rapid requests to verify consistency
        responses = []
        for _ in range(3):
            response = requests.get(f"{api_base_url}/health")
            responses.append(response)
            time.sleep(0.5)  # Small delay between requests
        
        # All responses should be successful
        for response in responses:
            assert response.status_code in [200, 206, 503]
        
        # Step 4: Verify uptime calculation
        if 'uptime_seconds' in detailed_health:
            assert detailed_health['uptime_seconds'] >= 0
            if 'uptime_hours' in detailed_health:
                expected_hours = detailed_health['uptime_seconds'] / 3600
                assert abs(detailed_health['uptime_hours'] - expected_hours) < 0.01
    
    def test_data_consistency_across_endpoints(self, api_base_url):
        """
        Test data consistency across different endpoints
        **Requirements: 6.1, 6.2, 6.3**
        """
        # Step 1: Get all skills
        response = requests.get(f"{api_base_url}/skills")
        assert response.status_code == 200
        skills_data = response.json()
        skills = skills_data['skills']
        
        # Step 2: Get all projects
        response = requests.get(f"{api_base_url}/projects")
        assert response.status_code == 200
        projects_data = response.json()
        projects = projects_data['projects']
        
        # Step 3: Get all certifications
        response = requests.get(f"{api_base_url}/certifications")
        assert response.status_code == 200
        certs_data = response.json()
        certifications = certs_data['certifications']
        
        # Step 4: Verify cross-references
        skill_names = {skill['name'].lower() for skill in skills}
        
        # Check if project technologies reference existing skills
        for project in projects:
            technologies = project.get('technologies', [])
            for tech in technologies:
                # This is a soft check - not all technologies need to be skills
                if tech.lower() in skill_names:
                    # If it matches a skill, that's good consistency
                    pass
        
        # Step 5: Verify certification-skill relationships
        for cert in certifications:
            if 'skills_validated' in cert:
                for skill_name in cert['skills_validated']:
                    # Soft check - skills validated by certs should ideally exist as skills
                    if skill_name.lower() in skill_names:
                        # Good consistency
                        pass
        
        # Step 6: Verify data freshness
        for skill in skills:
            if 'updated_at' in skill:
                updated_at = datetime.fromisoformat(skill['updated_at'].replace('Z', ''))
                # Data should not be older than 1 year (reasonable freshness)
                age_days = (datetime.utcnow() - updated_at).days
                assert age_days < 365
    
    def test_error_handling_scenarios(self, api_base_url):
        """
        Test error handling scenarios with external service failures
        **Requirements: 3.5, 4.2, 5.1**
        """
        # Step 1: Test invalid endpoint
        response = requests.get(f"{api_base_url}/nonexistent")
        assert response.status_code == 404
        
        # Step 2: Test invalid query parameters
        response = requests.get(f"{api_base_url}/skills?category=invalid_category")
        # Should return empty results, not error
        assert response.status_code == 200
        data = response.json()
        # Should return empty or filtered results
        assert 'skills' in data
        
        # Step 3: Test malformed requests
        response = requests.get(f"{api_base_url}/certifications?provider=")
        # Should handle empty parameter gracefully
        assert response.status_code == 200
        
        # Step 4: Test rate limiting behavior (if implemented)
        # Make multiple rapid requests
        responses = []
        for i in range(10):
            response = requests.get(f"{api_base_url}/health")
            responses.append(response.status_code)
        
        # Should not have too many failures due to rate limiting
        success_count = sum(1 for code in responses if code in [200, 206])
        assert success_count >= 7  # At least 70% success rate
        
        # Step 5: Test timeout scenarios (if health endpoint has external dependencies)
        start_time = time.time()
        response = requests.get(f"{api_base_url}/health?include_metrics=true", timeout=30)
        end_time = time.time()
        
        # Should respond within reasonable time
        response_time = end_time - start_time
        assert response_time < 30  # Should not timeout
        
        # Even if some metrics fail, should still return a response
        assert response.status_code in [200, 206, 503]
    
    def test_system_performance_characteristics(self, api_base_url):
        """
        Test system performance characteristics
        **Requirements: 5.5**
        """
        # Step 1: Measure response times for different endpoints
        endpoints = ['/skills', '/projects', '/certifications', '/health']
        response_times = {}
        
        for endpoint in endpoints:
            start_time = time.time()
            response = requests.get(f"{api_base_url}{endpoint}")
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            response_times[endpoint] = response_time
            
            # Verify response time is reasonable (under 5 seconds)
            assert response_time < 5000
            assert response.status_code in [200, 206]
        
        # Step 2: Test concurrent requests
        import concurrent.futures
        
        def make_request(endpoint):
            start_time = time.time()
            response = requests.get(f"{api_base_url}{endpoint}")
            end_time = time.time()
            return {
                'endpoint': endpoint,
                'status_code': response.status_code,
                'response_time': (end_time - start_time) * 1000
            }
        
        # Make 5 concurrent requests to different endpoints
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request, endpoint) for endpoint in endpoints[:5]]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # Verify all concurrent requests succeeded
        for result in results:
            assert result['status_code'] in [200, 206]
            assert result['response_time'] < 10000  # 10 seconds max under load
        
        # Step 3: Verify system remains responsive
        # Make a final health check
        response = requests.get(f"{api_base_url}/health")
        assert response.status_code in [200, 206, 503]
        
        health_data = response.json()
        assert 'status' in health_data
        
        # System should still be operational
        assert health_data['status'] in ['healthy', 'degraded']


@pytest.mark.integration
class TestSystemValidation:
    """System-wide validation tests"""
    
    def test_all_required_endpoints_available(self, api_base_url="https://api.oyins-journey.dev"):
        """Verify all required endpoints are available and functional"""
        required_endpoints = [
            '/skills',
            '/projects', 
            '/certifications',
            '/adrs',
            '/health'
        ]
        
        for endpoint in required_endpoints:
            response = requests.get(f"{api_base_url}{endpoint}")
            assert response.status_code in [200, 206], f"Endpoint {endpoint} is not available"
            
            # Verify response is valid JSON
            try:
                data = response.json()
                assert isinstance(data, dict)
            except json.JSONDecodeError:
                pytest.fail(f"Endpoint {endpoint} did not return valid JSON")
    
    def test_system_metadata_consistency(self, api_base_url="https://api.oyins-journey.dev"):
        """Verify system metadata is consistent across endpoints"""
        # Get health info
        response = requests.get(f"{api_base_url}/health")
        assert response.status_code in [200, 206]
        
        health_data = response.json()
        
        # Verify basic system info
        if 'system_info' in health_data:
            system_info = health_data['system_info']
            assert 'version' in system_info
            assert system_info['version'].startswith('v') or system_info['version'][0].isdigit()
        
        # Verify timestamp format consistency
        assert 'timestamp' in health_data
        timestamp_str = health_data['timestamp']
        
        # Should be ISO format
        try:
            datetime.fromisoformat(timestamp_str.replace('Z', ''))
        except ValueError:
            pytest.fail(f"Invalid timestamp format: {timestamp_str}")


if __name__ == '__main__':
    # Run integration tests
    pytest.main([__file__, '-v', '--tb=short'])