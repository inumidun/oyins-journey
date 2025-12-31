"""
Evidence Link Validation and Enrichment Service
Handles validation of evidence links and enrichment of project/skill data
"""

import json
import requests
import boto3
import os
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import time

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')

def validate_single_link(link_data, timeout=10):
    """
    Validate a single evidence link
    """
    url = link_data.get('url', '')
    link_type = link_data.get('type', 'unknown')
    
    result = {
        'url': url,
        'type': link_type,
        'status': 'unknown',
        'last_checked': datetime.utcnow().isoformat() + 'Z',
        'response_time_ms': None,
        'error_message': None
    }
    
    try:
        # Validate URL format
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            result['status'] = 'error'
            result['error_message'] = 'Invalid URL format'
            return result
        
        # Make request with timeout
        start_time = time.time()
        
        # Use HEAD request first for efficiency, fallback to GET
        try:
            response = requests.head(url, timeout=timeout, allow_redirects=True)
        except requests.exceptions.RequestException:
            response = requests.get(url, timeout=timeout, allow_redirects=True)
        
        end_time = time.time()
        result['response_time_ms'] = round((end_time - start_time) * 1000, 2)
        
        # Check response status
        if response.status_code == 200:
            result['status'] = 'active'
        elif response.status_code in [301, 302, 307, 308]:
            result['status'] = 'active'  # Redirects are OK
            result['redirect_url'] = response.url
        elif response.status_code in [404, 410]:
            result['status'] = 'inactive'
            result['error_message'] = f'HTTP {response.status_code}'
        elif response.status_code == 403:
            result['status'] = 'restricted'
            result['error_message'] = 'Access forbidden'
        elif response.status_code >= 500:
            result['status'] = 'server_error'
            result['error_message'] = f'Server error: HTTP {response.status_code}'
        else:
            result['status'] = 'unknown'
            result['error_message'] = f'HTTP {response.status_code}'
            
    except requests.exceptions.Timeout:
        result['status'] = 'timeout'
        result['error_message'] = 'Request timed out'
    except requests.exceptions.ConnectionError:
        result['status'] = 'connection_error'
        result['error_message'] = 'Connection failed'
    except requests.exceptions.InvalidURL:
        result['status'] = 'error'
        result['error_message'] = 'Invalid URL'
    except Exception as e:
        result['status'] = 'error'
        result['error_message'] = str(e)
    
    return result

def validate_evidence_links(links, max_workers=5, timeout=10):
    """
    Validate multiple evidence links concurrently
    """
    if not links:
        return []
    
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all validation tasks
        future_to_link = {
            executor.submit(validate_single_link, link, timeout): link 
            for link in links
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_link):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                # If validation fails completely, create error result
                link = future_to_link[future]
                error_result = {
                    'url': link.get('url', ''),
                    'type': link.get('type', 'unknown'),
                    'status': 'error',
                    'last_checked': datetime.utcnow().isoformat() + 'Z',
                    'error_message': f'Validation failed: {str(e)}'
                }
                results.append(error_result)
    
    # Sort results to match original order
    url_to_result = {result['url']: result for result in results}
    ordered_results = []
    for link in links:
        url = link.get('url', '')
        if url in url_to_result:
            ordered_results.append(url_to_result[url])
        else:
            # Fallback if somehow missing
            ordered_results.append({
                'url': url,
                'type': link.get('type', 'unknown'),
                'status': 'error',
                'last_checked': datetime.utcnow().isoformat() + 'Z',
                'error_message': 'Validation result missing'
            })
    
    return ordered_results

def validate_evidence_links_batch(links, batch_size=10, max_workers=5, timeout=10):
    """
    Validate evidence links in batches for better performance with large sets
    """
    if not links:
        return []
    
    all_results = []
    
    # Process in batches
    for i in range(0, len(links), batch_size):
        batch = links[i:i + batch_size]
        batch_results = validate_evidence_links(batch, max_workers, timeout)
        all_results.extend(batch_results)
        
        # Small delay between batches to be respectful to servers
        if i + batch_size < len(links):
            time.sleep(0.1)
    
    return all_results

def get_github_stats(github_url):
    """
    Get GitHub repository statistics (reused from projects.py)
    """
    try:
        if not github_url or 'github.com' not in github_url:
            return None
            
        # Extract owner and repo from GitHub URL
        parts = github_url.rstrip('/').split('/')
        if len(parts) < 5:
            return None
            
        owner = parts[-2]
        repo = parts[-1]
        
        # GitHub API endpoints
        repo_api_url = f"https://api.github.com/repos/{owner}/{repo}"
        commits_api_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        actions_api_url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
        
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Living-Architecture-Resume/1.0'
        }
        
        # Add GitHub token if available
        github_token = os.environ.get('GITHUB_TOKEN')
        if github_token:
            headers['Authorization'] = f'token {github_token}'
        
        # Fetch repository information
        repo_response = requests.get(repo_api_url, headers=headers, timeout=10)
        if repo_response.status_code != 200:
            return None
            
        repo_data = repo_response.json()
        
        # Fetch recent commits
        since_date = (datetime.now() - timedelta(days=30)).isoformat()
        commits_params = {'since': since_date, 'per_page': 100}
        commits_response = requests.get(commits_api_url, headers=headers, params=commits_params, timeout=10)
        
        commits_data = []
        if commits_response.status_code == 200:
            commits_data = commits_response.json()
        
        # Fetch GitHub Actions status
        actions_response = requests.get(actions_api_url, headers=headers, params={'per_page': 1}, timeout=10)
        pipeline_status = 'unknown'
        last_build = None
        
        if actions_response.status_code == 200:
            actions_data = actions_response.json()
            if actions_data.get('workflow_runs'):
                latest_run = actions_data['workflow_runs'][0]
                pipeline_status = latest_run.get('conclusion', 'unknown')
                last_build = latest_run.get('updated_at')
        
        return {
            'stars': repo_data.get('stargazers_count', 0),
            'forks': repo_data.get('forks_count', 0),
            'open_issues': repo_data.get('open_issues_count', 0),
            'language': repo_data.get('language'),
            'topics': repo_data.get('topics', []),
            'last_updated': repo_data.get('updated_at'),
            'commits_last_30_days': len(commits_data),
            'recent_commits': [
                {
                    'sha': commit['sha'][:7],
                    'message': commit['commit']['message'].split('\n')[0][:100],
                    'date': commit['commit']['author']['date'],
                    'author': commit['commit']['author']['name']
                }
                for commit in commits_data[:5]
            ],
            'pipeline_status': pipeline_status,
            'last_build': last_build
        }
        
    except Exception as e:
        print(f"Error fetching GitHub stats for {github_url}: {str(e)}")
        return None

def enrich_project_evidence(project_data):
    """
    Enrich project data with validated evidence links and GitHub stats
    """
    enriched_project = project_data.copy()
    
    # Validate evidence links if they exist
    evidence_links = project_data.get('evidence_links', [])
    if evidence_links:
        validated_links = validate_evidence_links(evidence_links)
        enriched_project['evidence_links'] = validated_links
        
        # Add evidence summary
        active_links = sum(1 for link in validated_links if link['status'] == 'active')
        enriched_project['evidence_summary'] = {
            'total_links': len(validated_links),
            'active_links': active_links,
            'validation_date': datetime.utcnow().isoformat() + 'Z'
        }
    
    # Enrich with GitHub data if GitHub URL exists
    github_url = project_data.get('github_url') or project_data.get('repository_url')
    if github_url:
        github_stats = get_github_stats(github_url)
        if github_stats:
            enriched_project['github_stats'] = github_stats
    
    return enriched_project

def get_related_projects(skill_name, projects_table_name=None):
    """
    Get projects related to a specific skill
    """
    try:
        if not projects_table_name:
            projects_table_name = os.environ.get('PROJECTS_TABLE', 'oyins-journey-projects')
        
        projects_table = dynamodb.Table(projects_table_name)
        response = projects_table.scan()
        
        related_projects = []
        for project in response['Items']:
            technologies = project.get('technologies', [])
            if any(skill_name.lower() in tech.lower() for tech in technologies):
                related_projects.append(project)
        
        return related_projects
        
    except Exception as e:
        print(f"Error getting related projects for skill {skill_name}: {str(e)}")
        return []

def enrich_skill_evidence(skill_data):
    """
    Enrich skill data with validated evidence links and related projects
    """
    enriched_skill = skill_data.copy()
    
    # Validate evidence links if they exist
    evidence_links = skill_data.get('evidence_links', [])
    if evidence_links:
        validated_links = validate_evidence_links(evidence_links)
        enriched_skill['evidence_links'] = validated_links
    else:
        validated_links = []
    
    # Get related projects
    skill_name = skill_data.get('name', '')
    if skill_name:
        related_projects = get_related_projects(skill_name)
        if related_projects:
            enriched_skill['related_projects'] = related_projects[:5]  # Limit to 5 most relevant
    
    # Create evidence summary
    active_links = sum(1 for link in validated_links if link['status'] == 'active')
    has_code_examples = any(
        link['type'] == 'repository' and link['status'] == 'active' 
        for link in validated_links
    )
    
    enriched_skill['evidence_summary'] = {
        'total_links': len(validated_links),
        'active_links': active_links,
        'has_code_examples': has_code_examples,
        'related_projects_count': len(enriched_skill.get('related_projects', [])),
        'validation_date': datetime.utcnow().isoformat() + 'Z'
    }
    
    return enriched_skill

def lambda_handler(event, context):
    """
    Lambda handler for evidence link validation service
    """
    try:
        # Parse request
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '')
        query_params = event.get('queryStringParameters') or {}
        
        if http_method == 'POST' and '/validate' in path:
            # Validate evidence links
            body = json.loads(event.get('body', '{}'))
            links = body.get('links', [])
            
            if not links:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'error': 'No links provided for validation'
                    })
                }
            
            # Validate links
            timeout = int(query_params.get('timeout', 10))
            max_workers = int(query_params.get('max_workers', 5))
            
            validation_results = validate_evidence_links(links, max_workers, timeout)
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'results': validation_results,
                    'summary': {
                        'total_links': len(validation_results),
                        'active_links': sum(1 for r in validation_results if r['status'] == 'active'),
                        'inactive_links': sum(1 for r in validation_results if r['status'] == 'inactive'),
                        'error_links': sum(1 for r in validation_results if r['status'] == 'error'),
                        'validation_date': datetime.utcnow().isoformat() + 'Z'
                    }
                })
            }
        
        else:
            # Default health check
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'service': 'Evidence Link Validator',
                    'status': 'healthy',
                    'version': '1.0.0',
                    'endpoints': [
                        'POST /validate - Validate evidence links'
                    ]
                })
            }
            
    except Exception as e:
        print(f"Error in evidence linker handler: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e) if os.environ.get('DEBUG') else 'An error occurred'
            })
        }