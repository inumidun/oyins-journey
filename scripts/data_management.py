#!/usr/bin/env python3
"""
Enhanced Data Management and Population Scripts
Handles data seeding, validation, and migration for the Living Architecture Resume system
"""

import json
import boto3
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import argparse
from botocore.exceptions import ClientError

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')

# Table configurations
TABLES = {
    'skills': {
        'name': os.environ.get('SKILLS_TABLE', 'oyins-journey-skills'),
        'key': 'skill_id',
        'gsi': 'CategoryIndex'
    },
    'projects': {
        'name': os.environ.get('PROJECTS_TABLE', 'oyins-journey-projects'),
        'key': 'project_id'
    },
    'certifications': {
        'name': os.environ.get('CERTIFICATIONS_TABLE', 'oyins-journey-certifications'),
        'key': 'id',
        'gsi': 'ProviderIndex'
    },
    'adrs': {
        'name': os.environ.get('ADRS_TABLE', 'oyins-journey-adrs'),
        'key': 'adr_id'
    }
}

def get_table(table_type: str):
    """Get DynamoDB table resource"""
    if table_type not in TABLES:
        raise ValueError(f"Unknown table type: {table_type}")
    
    table_config = TABLES[table_type]
    return dynamodb.Table(table_config['name'])

def validate_item_schema(item: Dict[str, Any], item_type: str) -> bool:
    """Validate item against expected schema"""
    required_fields = {
        'skills': ['skill_id', 'name', 'category'],
        'projects': ['project_id', 'name', 'description'],
        'certifications': ['id', 'name', 'provider'],
        'adrs': ['adr_id', 'title', 'status']
    }
    
    if item_type not in required_fields:
        return False
    
    for field in required_fields[item_type]:
        if field not in item:
            print(f"Missing required field '{field}' in {item_type} item")
            return False
    
    return True

def add_timestamps(item: Dict[str, Any]) -> Dict[str, Any]:
    """Add created_at and updated_at timestamps to item"""
    now = datetime.utcnow().isoformat() + 'Z'
    
    if 'created_at' not in item:
        item['created_at'] = now
    
    item['updated_at'] = now
    return item

def populate_skills_data():
    """Populate skills table with comprehensive professional data"""
    skills_data = [
        {
            'skill_id': 'aws-lambda',
            'name': 'AWS Lambda',
            'category': 'cloud',
            'cloud': 'aws',
            'proficiency': 'advanced',
            'years_experience': 3,
            'technologies': ['Python', 'Node.js', 'TypeScript'],
            'evidence_links': [
                {
                    'type': 'repository',
                    'url': 'https://github.com/oyintech/lambda-examples',
                    'description': 'Lambda function examples and patterns'
                }
            ],
            'projects': ['oyins-journey', 'serverless-api'],
            'certifications': ['aws-saa-c03']
        },
        {
            'skill_id': 'dynamodb',
            'name': 'Amazon DynamoDB',
            'category': 'database',
            'cloud': 'aws',
            'proficiency': 'advanced',
            'years_experience': 3,
            'technologies': ['NoSQL', 'Python', 'JavaScript'],
            'evidence_links': [
                {
                    'type': 'repository',
                    'url': 'https://github.com/oyintech/dynamodb-patterns',
                    'description': 'DynamoDB design patterns and examples'
                }
            ],
            'projects': ['oyins-journey', 'data-pipeline'],
            'certifications': ['aws-saa-c03']
        },
        {
            'skill_id': 'terraform',
            'name': 'Terraform',
            'category': 'devops',
            'proficiency': 'advanced',
            'years_experience': 4,
            'technologies': ['HCL', 'AWS', 'Infrastructure as Code'],
            'evidence_links': [
                {
                    'type': 'repository',
                    'url': 'https://github.com/oyintech/terraform-modules',
                    'description': 'Reusable Terraform modules'
                }
            ],
            'projects': ['infrastructure-automation', 'multi-env-deployment']
        },
        {
            'skill_id': 'python',
            'name': 'Python',
            'category': 'programming',
            'proficiency': 'expert',
            'years_experience': 8,
            'technologies': ['FastAPI', 'Django', 'Flask', 'Pandas', 'NumPy'],
            'evidence_links': [
                {
                    'type': 'repository',
                    'url': 'https://github.com/oyintech/python-projects',
                    'description': 'Python projects and libraries'
                }
            ],
            'projects': ['data-analysis-tool', 'api-gateway', 'ml-pipeline']
        },
        {
            'skill_id': 'typescript',
            'name': 'TypeScript',
            'category': 'programming',
            'proficiency': 'advanced',
            'years_experience': 4,
            'technologies': ['React', 'Node.js', 'Express', 'Vite'],
            'evidence_links': [
                {
                    'type': 'repository',
                    'url': 'https://github.com/oyintech/typescript-examples',
                    'description': 'TypeScript patterns and best practices'
                }
            ],
            'projects': ['frontend-dashboard', 'api-client', 'oyins-journey']
        },
        {
            'skill_id': 'docker',
            'name': 'Docker',
            'category': 'devops',
            'proficiency': 'advanced',
            'years_experience': 5,
            'technologies': ['Containerization', 'Docker Compose', 'Multi-stage builds'],
            'evidence_links': [
                {
                    'type': 'repository',
                    'url': 'https://github.com/oyintech/docker-templates',
                    'description': 'Docker templates and configurations'
                }
            ],
            'projects': ['microservices-platform', 'development-environment']
        },
        {
            'skill_id': 'github-actions',
            'name': 'GitHub Actions',
            'category': 'devops',
            'proficiency': 'advanced',
            'years_experience': 3,
            'technologies': ['CI/CD', 'YAML', 'Automation'],
            'evidence_links': [
                {
                    'type': 'repository',
                    'url': 'https://github.com/oyintech/github-actions-workflows',
                    'description': 'Reusable GitHub Actions workflows'
                }
            ],
            'projects': ['oyins-journey', 'automated-deployment']
        }
    ]
    
    table = get_table('skills')
    
    for skill in skills_data:
        skill = add_timestamps(skill)
        if validate_item_schema(skill, 'skills'):
            try:
                table.put_item(Item=skill)
                print(f"✓ Added skill: {skill['name']}")
            except ClientError as e:
                print(f"✗ Failed to add skill {skill['name']}: {e}")
        else:
            print(f"✗ Invalid schema for skill: {skill.get('name', 'Unknown')}")

def populate_projects_data():
    """Populate projects table with real project data"""
    projects_data = [
        {
            'project_id': 'oyins-journey',
            'name': "Oyin's Journey - Living Architecture Resume",
            'description': 'A serverless, queryable CV system that demonstrates cloud architecture skills through its own implementation',
            'status': 'active',
            'start_date': '2024-01-01',
            'end_date': None,
            'technologies': ['AWS Lambda', 'DynamoDB', 'API Gateway', 'React', 'TypeScript', 'Terraform'],
            'github_url': 'https://github.com/oyintech/oyins-journey',
            'demo_url': 'https://oyins-journey.dev',
            'evidence_links': [
                {
                    'type': 'repository',
                    'url': 'https://github.com/oyintech/oyins-journey',
                    'description': 'Main project repository'
                },
                {
                    'type': 'demo',
                    'url': 'https://oyins-journey.dev',
                    'description': 'Live deployment'
                },
                {
                    'type': 'pipeline',
                    'url': 'https://github.com/oyintech/oyins-journey/actions',
                    'description': 'CI/CD pipeline'
                }
            ],
            'key_achievements': [
                'Implemented serverless architecture with 99.9% uptime',
                'Achieved sub-200ms API response times',
                'Automated deployment with GitHub Actions',
                'Integrated real-time monitoring and observability'
            ]
        },
        {
            'project_id': 'serverless-api',
            'name': 'Enterprise Serverless API Platform',
            'description': 'Scalable serverless API platform handling millions of requests per month',
            'status': 'completed',
            'start_date': '2023-06-01',
            'end_date': '2024-03-01',
            'technologies': ['AWS Lambda', 'API Gateway', 'DynamoDB', 'CloudWatch', 'Python'],
            'evidence_links': [
                {
                    'type': 'documentation',
                    'url': 'https://docs.example.com/serverless-api',
                    'description': 'API documentation and architecture'
                }
            ],
            'key_achievements': [
                'Reduced infrastructure costs by 60%',
                'Improved API response times by 40%',
                'Implemented comprehensive monitoring and alerting'
            ]
        },
        {
            'project_id': 'infrastructure-automation',
            'name': 'Multi-Environment Infrastructure Automation',
            'description': 'Terraform-based infrastructure automation for multiple environments',
            'status': 'active',
            'start_date': '2023-01-01',
            'technologies': ['Terraform', 'AWS', 'GitHub Actions', 'Python'],
            'evidence_links': [
                {
                    'type': 'repository',
                    'url': 'https://github.com/oyintech/terraform-infrastructure',
                    'description': 'Infrastructure as Code repository'
                }
            ],
            'key_achievements': [
                'Automated deployment across 5 environments',
                'Reduced deployment time from hours to minutes',
                'Implemented infrastructure drift detection'
            ]
        }
    ]
    
    table = get_table('projects')
    
    for project in projects_data:
        project = add_timestamps(project)
        if validate_item_schema(project, 'projects'):
            try:
                table.put_item(Item=project)
                print(f"✓ Added project: {project['name']}")
            except ClientError as e:
                print(f"✗ Failed to add project {project['name']}: {e}")
        else:
            print(f"✗ Invalid schema for project: {project.get('name', 'Unknown')}")

def populate_adrs_data():
    """Populate ADRs table with architectural decisions"""
    adrs_data = [
        {
            'adr_id': 'adr-001',
            'title': 'Use Serverless Architecture for CV System',
            'status': 'accepted',
            'date': '2024-01-15',
            'context': 'Need to build a cost-effective, scalable system that demonstrates cloud architecture skills',
            'decision': 'Use AWS Lambda, API Gateway, and DynamoDB for a serverless architecture',
            'consequences': [
                'Positive: Low operational overhead and cost',
                'Positive: Automatic scaling',
                'Negative: Cold start latency',
                'Negative: Vendor lock-in to AWS'
            ],
            'tags': ['architecture', 'serverless', 'aws']
        },
        {
            'adr_id': 'adr-002',
            'title': 'Use DynamoDB for Data Storage',
            'status': 'accepted',
            'date': '2024-01-20',
            'context': 'Need a database solution that fits serverless architecture and provides fast access',
            'decision': 'Use Amazon DynamoDB with appropriate GSI design for query patterns',
            'consequences': [
                'Positive: Serverless and fully managed',
                'Positive: Consistent performance at scale',
                'Negative: NoSQL limitations for complex queries',
                'Negative: Requires careful schema design'
            ],
            'tags': ['database', 'dynamodb', 'nosql']
        },
        {
            'adr_id': 'adr-003',
            'title': 'Implement Property-Based Testing',
            'status': 'accepted',
            'date': '2024-02-01',
            'context': 'Need comprehensive testing strategy that validates correctness across all inputs',
            'decision': 'Use property-based testing alongside unit tests for comprehensive coverage',
            'consequences': [
                'Positive: Better test coverage and bug detection',
                'Positive: Validates correctness properties',
                'Negative: Steeper learning curve',
                'Negative: Longer test execution times'
            ],
            'tags': ['testing', 'quality', 'property-based-testing']
        }
    ]
    
    table = get_table('adrs')
    
    for adr in adrs_data:
        adr = add_timestamps(adr)
        if validate_item_schema(adr, 'adrs'):
            try:
                table.put_item(Item=adr)
                print(f"✓ Added ADR: {adr['title']}")
            except ClientError as e:
                print(f"✗ Failed to add ADR {adr['title']}: {e}")
        else:
            print(f"✗ Invalid schema for ADR: {adr.get('title', 'Unknown')}")

def validate_data_integrity():
    """Validate data integrity across all tables"""
    print("\n=== Data Integrity Validation ===")
    
    # Check skills table
    skills_table = get_table('skills')
    try:
        skills_response = skills_table.scan()
        skills = skills_response['Items']
        print(f"✓ Skills table: {len(skills)} items")
        
        # Validate skill references in projects
        projects_table = get_table('projects')
        projects_response = projects_table.scan()
        projects = projects_response['Items']
        
        skill_names = {skill['name'].lower() for skill in skills}
        
        for project in projects:
            project_technologies = [tech.lower() for tech in project.get('technologies', [])]
            referenced_skills = [tech for tech in project_technologies if tech in skill_names]
            if referenced_skills:
                print(f"  ✓ Project '{project['name']}' references {len(referenced_skills)} skills")
        
    except ClientError as e:
        print(f"✗ Error validating skills: {e}")
    
    # Check certifications table
    try:
        certifications_table = get_table('certifications')
        certifications_response = certifications_table.scan()
        certifications = certifications_response['Items']
        print(f"✓ Certifications table: {len(certifications)} items")
        
        # Check expiry status calculation
        now = datetime.utcnow()
        for cert in certifications:
            if 'expiry_date' in cert:
                expiry_date = datetime.fromisoformat(cert['expiry_date'].replace('Z', ''))
                is_expired = expiry_date < now
                computed_status = cert.get('computed_status', 'unknown')
                
                if is_expired and computed_status != 'expired':
                    print(f"  ⚠ Certification '{cert['name']}' may have incorrect status")
                elif not is_expired and computed_status == 'expired':
                    print(f"  ⚠ Certification '{cert['name']}' may have incorrect status")
        
    except ClientError as e:
        print(f"✗ Error validating certifications: {e}")
    
    # Check projects table
    try:
        print(f"✓ Projects table: {len(projects)} items")
        
        # Validate GitHub URLs
        for project in projects:
            github_url = project.get('github_url')
            if github_url and 'github.com' not in github_url:
                print(f"  ⚠ Project '{project['name']}' has invalid GitHub URL")
        
    except ClientError as e:
        print(f"✗ Error validating projects: {e}")
    
    # Check ADRs table
    try:
        adrs_table = get_table('adrs')
        adrs_response = adrs_table.scan()
        adrs = adrs_response['Items']
        print(f"✓ ADRs table: {len(adrs)} items")
        
        # Validate ADR status values
        valid_statuses = ['proposed', 'accepted', 'deprecated', 'superseded']
        for adr in adrs:
            if adr.get('status') not in valid_statuses:
                print(f"  ⚠ ADR '{adr['title']}' has invalid status: {adr.get('status')}")
        
    except ClientError as e:
        print(f"✗ Error validating ADRs: {e}")

def backup_table_data(table_type: str, backup_file: str):
    """Backup table data to JSON file"""
    table = get_table(table_type)
    
    try:
        response = table.scan()
        items = response['Items']
        
        # Handle pagination
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])
        
        # Convert Decimal types to float for JSON serialization
        def decimal_default(obj):
            if hasattr(obj, '__float__'):
                return float(obj)
            raise TypeError
        
        with open(backup_file, 'w') as f:
            json.dump(items, f, indent=2, default=decimal_default)
        
        print(f"✓ Backed up {len(items)} items from {table_type} table to {backup_file}")
        
    except ClientError as e:
        print(f"✗ Failed to backup {table_type} table: {e}")

def restore_table_data(table_type: str, backup_file: str):
    """Restore table data from JSON file"""
    if not os.path.exists(backup_file):
        print(f"✗ Backup file {backup_file} not found")
        return
    
    table = get_table(table_type)
    
    try:
        with open(backup_file, 'r') as f:
            items = json.load(f)
        
        for item in items:
            table.put_item(Item=item)
        
        print(f"✓ Restored {len(items)} items to {table_type} table from {backup_file}")
        
    except (ClientError, json.JSONDecodeError) as e:
        print(f"✗ Failed to restore {table_type} table: {e}")

def main():
    parser = argparse.ArgumentParser(description='Data Management for Living Architecture Resume')
    parser.add_argument('action', choices=[
        'populate-all', 'populate-skills', 'populate-projects', 'populate-certifications', 'populate-adrs',
        'validate', 'backup', 'restore'
    ], help='Action to perform')
    parser.add_argument('--table', choices=['skills', 'projects', 'certifications', 'adrs'], 
                       help='Specific table for backup/restore operations')
    parser.add_argument('--file', help='Backup/restore file path')
    
    args = parser.parse_args()
    
    if args.action == 'populate-all':
        print("=== Populating All Tables ===")
        populate_skills_data()
        populate_projects_data()
        populate_adrs_data()
        # Note: Certifications are populated by separate script
        print("\n=== Population Complete ===")
        validate_data_integrity()
        
    elif args.action == 'populate-skills':
        populate_skills_data()
        
    elif args.action == 'populate-projects':
        populate_projects_data()
        
    elif args.action == 'populate-adrs':
        populate_adrs_data()
        
    elif args.action == 'validate':
        validate_data_integrity()
        
    elif args.action == 'backup':
        if not args.table or not args.file:
            print("✗ --table and --file are required for backup")
            sys.exit(1)
        backup_table_data(args.table, args.file)
        
    elif args.action == 'restore':
        if not args.table or not args.file:
            print("✗ --table and --file are required for restore")
            sys.exit(1)
        restore_table_data(args.table, args.file)

if __name__ == '__main__':
    main()