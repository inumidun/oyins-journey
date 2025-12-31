"""
Property-based tests for evidence link validation functionality.
Feature: living-architecture-resume-enhancement
"""

import pytest
from hypothesis import given, strategies as st, settings
import json
import requests
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta


class TestEvidenceLinkProperties:
    
    # Property 9: Evidence Link Validation
    # Feature: living-architecture-resume-enhancement, Property 9: For any evidence link, the system should validate accessibility and display appropriate status and messaging for unavailable resources
    @given(
        evidence_links=st.lists(
            st.fixed_dictionaries({
                'type': st.sampled_from(['repository', 'demo', 'pipeline', 'dashboard', 'documentation']),
                'url': st.one_of(
                    st.text(min_size=1).map(lambda x: f"https://github.com/user/{x}"),
                    st.text(min_size=1).map(lambda x: f"https://example.com/{x}"),
                    st.just("invalid-url"),
                    st.just("https://nonexistent-domain-12345.com/test")
                ),
                'description': st.text(min_size=1, max_size=100)
            }),
            min_size=1,
            max_size=10
        )
    )
    @settings(max_examples=100)
    def test_evidence_link_validation_property(self, evidence_links):
        """
        Property 9: For any evidence link, the system should validate accessibility 
        and display appropriate status and messaging for unavailable resources
        **Validates: Requirements 4.1, 4.2, 4.5**
        """
        from api.evidence_linker import validate_evidence_links
        
        # Mock different response scenarios
        def mock_requests_get(url, **kwargs):
            mock_response = MagicMock()
            
            if "github.com" in url:
                mock_response.status_code = 200
                mock_response.json.return_value = {"message": "Repository accessible"}
            elif "nonexistent-domain" in url:
                mock_response.status_code = 404
                mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
            elif url == "invalid-url":
                raise requests.exceptions.InvalidURL("Invalid URL")
            else:
                mock_response.status_code = 200
                
            return mock_response
        
        with patch('requests.get', side_effect=mock_requests_get):
            with patch('requests.head', side_effect=mock_requests_get):
                validation_results = validate_evidence_links(evidence_links)
                
                # Verify that validation results are returned for all links
                assert len(validation_results) == len(evidence_links)
                
                # Verify each result has required fields
                for i, result in enumerate(validation_results):
                    original_link = evidence_links[i]
                    
                    assert 'url' in result
                    assert 'status' in result
                    assert 'last_checked' in result
                    assert 'type' in result
                    
                    # Verify URL matches original
                    assert result['url'] == original_link['url']
                    assert result['type'] == original_link['type']
                    
                    # Verify status is one of expected values
                    assert result['status'] in ['active', 'inactive', 'unknown', 'error']
                    
                    # Verify timestamp is recent
                    last_checked = datetime.fromisoformat(result['last_checked'].replace('Z', ''))
                    assert (datetime.utcnow() - last_checked).total_seconds() < 60
                    
                    # Verify appropriate status based on URL
                    if "github.com" in original_link['url']:
                        assert result['status'] == 'active'
                    elif "nonexistent-domain" in original_link['url']:
                        assert result['status'] == 'inactive'
                    elif original_link['url'] == "invalid-url":
                        assert result['status'] == 'error'

    # Property 10: Project Evidence Enrichment
    # Feature: living-architecture-resume-enhancement, Property 10: For any project display, the system should include GitHub commit activity and pipeline status information
    @given(
        project_data=st.fixed_dictionaries({
            'project_id': st.text(min_size=1, max_size=50),
            'name': st.text(min_size=1, max_size=100),
            'github_url': st.one_of(
                st.none(),
                st.text(min_size=1).map(lambda x: f"https://github.com/user/{x}")
            ),
            'evidence_links': st.lists(
                st.fixed_dictionaries({
                    'type': st.sampled_from(['repository', 'demo', 'pipeline']),
                    'url': st.text(min_size=1).map(lambda x: f"https://example.com/{x}")
                }),
                min_size=0,
                max_size=5
            )
        })
    )
    @settings(max_examples=100)
    def test_project_evidence_enrichment_property(self, project_data):
        """
        Property 10: For any project display, the system should include GitHub 
        commit activity and pipeline status information
        **Validates: Requirements 4.3**
        """
        from api.evidence_linker import enrich_project_evidence
        
        # Mock GitHub API responses
        mock_github_data = {
            'commits_last_30_days': 15,
            'recent_commits': [
                {
                    'sha': 'abc1234',
                    'message': 'Add new feature',
                    'date': '2024-12-30T10:00:00Z',
                    'author': 'developer'
                }
            ],
            'pipeline_status': 'success',
            'last_build': '2024-12-30T09:00:00Z'
        }
        
        with patch('api.evidence_linker.get_github_stats', return_value=mock_github_data):
            enriched_project = enrich_project_evidence(project_data)
            
            # Verify original project data is preserved
            assert enriched_project['project_id'] == project_data['project_id']
            assert enriched_project['name'] == project_data['name']
            
            # If project has GitHub URL, verify enrichment
            if project_data.get('github_url'):
                assert 'github_stats' in enriched_project
                assert 'commits_last_30_days' in enriched_project['github_stats']
                assert 'recent_commits' in enriched_project['github_stats']
                assert 'pipeline_status' in enriched_project['github_stats']
            
            # Verify evidence links are processed
            if project_data.get('evidence_links'):
                assert 'evidence_links' in enriched_project
                for link in enriched_project['evidence_links']:
                    assert 'status' in link
                    assert 'last_checked' in link

    # Property 11: Skills Evidence Linking
    # Feature: living-architecture-resume-enhancement, Property 11: For any skill entry, the system should provide links to specific code examples or implementation evidence
    @given(
        skill_data=st.fixed_dictionaries({
            'skill_id': st.text(min_size=1, max_size=50),
            'name': st.text(min_size=1, max_size=100),
            'category': st.sampled_from(['cloud', 'programming', 'database', 'devops']),
            'evidence_links': st.lists(
                st.fixed_dictionaries({
                    'type': st.sampled_from(['repository', 'documentation', 'demo']),
                    'url': st.text(min_size=1).map(lambda x: f"https://github.com/user/{x}"),
                    'description': st.text(min_size=1, max_size=100)
                }),
                min_size=0,
                max_size=5
            ),
            'projects': st.lists(st.text(min_size=1, max_size=50), min_size=0, max_size=3)
        })
    )
    @settings(max_examples=100)
    def test_skills_evidence_linking_property(self, skill_data):
        """
        Property 11: For any skill entry, the system should provide links to 
        specific code examples or implementation evidence
        **Validates: Requirements 4.4**
        """
        from api.evidence_linker import enrich_skill_evidence
        
        # Mock project data that might be linked to this skill
        mock_projects = [
            {
                'project_id': project_id,
                'name': f'Project {project_id}',
                'github_url': f'https://github.com/user/{project_id}',
                'technologies': [skill_data['name']]
            }
            for project_id in skill_data.get('projects', [])
        ]
        
        with patch('api.evidence_linker.get_related_projects', return_value=mock_projects):
            enriched_skill = enrich_skill_evidence(skill_data)
            
            # Verify original skill data is preserved
            assert enriched_skill['skill_id'] == skill_data['skill_id']
            assert enriched_skill['name'] == skill_data['name']
            assert enriched_skill['category'] == skill_data['category']
            
            # Verify evidence links are processed and validated
            if skill_data.get('evidence_links'):
                assert 'evidence_links' in enriched_skill
                for link in enriched_skill['evidence_links']:
                    assert 'status' in link
                    assert 'last_checked' in link
                    assert link['type'] in ['repository', 'documentation', 'demo']
            
            # Verify related projects are linked
            if skill_data.get('projects'):
                assert 'related_projects' in enriched_skill
                assert len(enriched_skill['related_projects']) <= len(skill_data['projects'])
                
                for project in enriched_skill['related_projects']:
                    assert 'project_id' in project
                    assert 'github_url' in project
                    assert skill_data['name'] in project.get('technologies', [])
            
            # Verify evidence summary is provided
            assert 'evidence_summary' in enriched_skill
            evidence_summary = enriched_skill['evidence_summary']
            assert 'total_links' in evidence_summary
            assert 'active_links' in evidence_summary
            assert 'has_code_examples' in evidence_summary

    @given(
        batch_links=st.lists(
            st.fixed_dictionaries({
                'url': st.one_of(
                    st.just("https://github.com/valid/repo"),
                    st.just("https://example.com/valid"),
                    st.just("https://timeout-site.com/slow"),
                    st.just("invalid-url-format"),
                    st.just("https://404-site.com/notfound")
                ),
                'type': st.sampled_from(['repository', 'demo', 'documentation'])
            }),
            min_size=1,
            max_size=20
        )
    )
    @settings(max_examples=100)
    def test_batch_link_validation_performance_property(self, batch_links):
        """
        Property: Batch link validation should handle multiple links efficiently
        and provide consistent results regardless of batch size
        **Validates: Requirements 4.1, 4.5**
        """
        from api.evidence_linker import validate_evidence_links_batch
        
        def mock_requests_get(url, **kwargs):
            mock_response = MagicMock()
            
            if "github.com" in url or "example.com" in url:
                mock_response.status_code = 200
            elif "timeout-site.com" in url:
                raise requests.exceptions.Timeout("Request timed out")
            elif "404-site.com" in url:
                mock_response.status_code = 404
                mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
            elif url == "invalid-url-format":
                raise requests.exceptions.InvalidURL("Invalid URL")
            else:
                mock_response.status_code = 200
                
            return mock_response
        
        with patch('requests.get', side_effect=mock_requests_get):
            with patch('requests.head', side_effect=mock_requests_get):
                start_time = datetime.utcnow()
                results = validate_evidence_links_batch(batch_links)
                end_time = datetime.utcnow()
                
                # Verify all links were processed
                assert len(results) == len(batch_links)
                
                # Verify processing time is reasonable (should be concurrent)
                processing_time = (end_time - start_time).total_seconds()
                # Allow generous time for testing, but ensure it's not sequential
                max_expected_time = min(30, len(batch_links) * 2)  # Much less than sequential
                assert processing_time < max_expected_time
                
                # Verify results consistency
                for i, result in enumerate(results):
                    original_link = batch_links[i]
                    assert result['url'] == original_link['url']
                    assert result['type'] == original_link['type']
                    assert result['status'] in ['active', 'inactive', 'error', 'timeout']
                    
                    # Verify status matches expected outcome
                    if "github.com" in original_link['url'] or "example.com" in original_link['url']:
                        assert result['status'] == 'active'
                    elif "timeout-site.com" in original_link['url']:
                        assert result['status'] == 'timeout'
                    elif "404-site.com" in original_link['url']:
                        assert result['status'] == 'inactive'
                    elif original_link['url'] == "invalid-url-format":
                        assert result['status'] == 'error'