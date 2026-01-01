import json
import boto3
import os
import requests
from boto3.dynamodb.conditions import Key
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
# Use environment variable for table name (no hardcoded environment)
table_name = os.environ.get('PROJECTS_TABLE', 'oyins-journey-projects')
projects_table = dynamodb.Table(table_name)

def get_github_stats(github_url):
    """
    Fetch GitHub repository statistics and commit activity
    """
    try:
        if not github_url or 'github.com' not in github_url:
            return None
            
        # Extract owner and repo from GitHub URL
        # Expected format: https://github.com/owner/repo
        parts = github_url.rstrip('/').split('/')
        if len(parts) < 5:
            return None
            
        owner = parts[-2]
        repo = parts[-1]
        
        # GitHub API endpoints
        repo_api_url = f"https://api.github.com/repos/{owner}/{repo}"
        commits_api_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        
        # Set timeout and headers
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
        
        # Fetch recent commits (last 30 days)
        since_date = (datetime.now() - timedelta(days=30)).isoformat()
        commits_params = {'since': since_date, 'per_page': 100}
        commits_response = requests.get(commits_api_url, headers=headers, params=commits_params, timeout=10)
        
        commits_data = []
        if commits_response.status_code == 200:
            commits_data = commits_response.json()
        
        # Extract relevant statistics
        github_stats = {
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
                for commit in commits_data[:5]  # Last 5 commits
            ]
        }
        
        return github_stats
        
    except requests.exceptions.Timeout:
        print(f"GitHub API timeout for {github_url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"GitHub API error for {github_url}: {str(e)}")
        return None
    except Exception as e:
        print(f"Error fetching GitHub stats for {github_url}: {str(e)}")
        return None

def enrich_project_with_github_data(project):
    """
    Enrich project data with GitHub statistics if GitHub URL is present
    """
    github_url = project.get('github_url') or project.get('repository_url')
    
    if github_url:
        github_stats = get_github_stats(github_url)
        if github_stats:
            project['github_stats'] = github_stats
            project['enriched_at'] = datetime.now().isoformat()
    
    return project

def lambda_handler(event, context):
    try:
        http_method = event.get('httpMethod', 'GET')
        
        if http_method == 'GET':
            return handle_get_projects(event)
        elif http_method == 'POST':
            return handle_create_project(event)
        else:
            return {
                'statusCode': 405,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Method not allowed'})
            }
            
    except Exception as e:
        print(f"Error in projects handler: {str(e)}")
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

def handle_get_projects(event):
    # Check if specific project ID requested
    path_params = event.get('pathParameters') or {}
    project_id = path_params.get('id')
    
    # Parse query parameters
    query_params = event.get('queryStringParameters') or {}
    include_github_data = query_params.get('include_github', 'true').lower() == 'true'
    
    if project_id:
        # Get specific project
        response = projects_table.get_item(
            Key={'project_id': project_id}
        )
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Project not found'
                })
            }
        
        project = response['Item']
        
        # Enrich with GitHub data if requested
        if include_github_data:
            project = enrich_project_with_github_data(project)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(project)
        }
    else:
        # Get all projects
        response = projects_table.scan()
        projects = response['Items']
        
        # Enrich with GitHub data if requested
        if include_github_data:
            enriched_projects = []
            for project in projects:
                try:
                    enriched_project = enrich_project_with_github_data(project)
                    enriched_projects.append(enriched_project)
                except Exception as e:
                    # If enrichment fails for one project, continue with others
                    print(f"Failed to enrich project {project.get('project_id', 'unknown')}: {str(e)}")
                    enriched_projects.append(project)
            projects = enriched_projects
        
        # Sort by date (newest first)
        projects.sort(key=lambda x: x.get('start_date', ''), reverse=True)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'projects': projects,
                'count': len(projects),
                'enriched': include_github_data
            })
        }

def handle_create_project(event):
    # Parse request body
    try:
        body = json.loads(event.get('body', '{}'))
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Invalid JSON in request body'})
        }
    
    # Validate required fields
    required_fields = ['name', 'description', 'status']
    for field in required_fields:
        if not body.get(field):
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': f'Missing required field: {field}'})
            }
    
    # Create project item
    import uuid
    project_id = body.get('project_id') or f"project-{uuid.uuid4().hex[:8]}"
    
    project_item = {
        'project_id': project_id,
        'name': body['name'],
        'description': body['description'],
        'status': body['status'],
        'technologies': body.get('technologies', []),
        'start_date': body.get('start_date', datetime.now().strftime('%Y-%m-%d')),
        'github_url': body.get('github_url', ''),
        'live_url': body.get('live_url', ''),
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    # Save to DynamoDB
    try:
        projects_table.put_item(Item=project_item)
        
        return {
            'statusCode': 201,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Project created successfully',
                'project': project_item
            })
        }
        
    except Exception as e:
        print(f"Error creating project: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Failed to create project',
                'message': str(e) if os.environ.get('DEBUG') else 'Database error'
            })
        }