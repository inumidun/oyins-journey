#!/usr/bin/env python3
"""
Sample data population script for Oyin's Journey CV system.
Populates DynamoDB tables with realistic CV data.
"""

import boto3
import json
from datetime import datetime, timedelta
import uuid

def get_table_name(base_name, environment='dev'):
    """Get environment-specific table name"""
    return f"oyins-journey-{environment}-{base_name}"

def populate_skills(dynamodb, environment='dev'):
    """Populate skills table with sample data"""
    table_name = get_table_name('skills', environment)
    table = dynamodb.Table(table_name)
    
    skills = [
        {
            'id': str(uuid.uuid4()),
            'name': 'AWS Lambda',
            'category': 'cloud',
            'technologies': ['Python', 'Node.js', 'Serverless'],
            'usage_count': 15,
            'proficiency': 'Expert',
            'years_experience': 3
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Terraform',
            'category': 'devops',
            'technologies': ['Infrastructure as Code', 'AWS', 'Azure'],
            'usage_count': 12,
            'proficiency': 'Advanced',
            'years_experience': 2
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Python',
            'category': 'programming',
            'technologies': ['FastAPI', 'Django', 'Flask', 'Pandas'],
            'usage_count': 25,
            'proficiency': 'Expert',
            'years_experience': 5
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'DynamoDB',
            'category': 'database',
            'technologies': ['NoSQL', 'AWS', 'Single Table Design'],
            'usage_count': 8,
            'proficiency': 'Advanced',
            'years_experience': 2
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'GitHub Actions',
            'category': 'devops',
            'technologies': ['CI/CD', 'Automation', 'YAML'],
            'usage_count': 10,
            'proficiency': 'Advanced',
            'years_experience': 2
        }
    ]
    
    for skill in skills:
        table.put_item(Item=skill)
    
    print(f"✅ Populated {len(skills)} skills")

def populate_projects(dynamodb, environment='dev'):
    """Populate projects table with sample data"""
    table_name = get_table_name('projects', environment)
    table = dynamodb.Table(table_name)
    
    projects = [
        {
            'id': str(uuid.uuid4()),
            'name': "Oyin's Journey - Living CV",
            'description': 'A cloud-native CV system that demonstrates real infrastructure skills',
            'status': 'active',
            'technologies': ['AWS Lambda', 'DynamoDB', 'Terraform', 'GitHub Actions'],
            'start_date': '2024-01-01',
            'end_date': None,
            'repository': 'https://github.com/inumidun/oyins-journey',
            'live_url': 'https://journey.oyintech.dev'
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Multi-Environment Infrastructure',
            'description': 'Terraform-based multi-environment AWS infrastructure with CI/CD',
            'status': 'completed',
            'technologies': ['Terraform', 'AWS', 'GitHub Actions', 'S3', 'CloudFront'],
            'start_date': '2023-11-01',
            'end_date': '2024-01-15',
            'repository': 'https://github.com/inumidun/infrastructure-template'
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Serverless API Gateway',
            'description': 'RESTful API using AWS Lambda and API Gateway with DynamoDB backend',
            'status': 'completed',
            'technologies': ['AWS Lambda', 'API Gateway', 'DynamoDB', 'Python'],
            'start_date': '2023-09-01',
            'end_date': '2023-12-01'
        }
    ]
    
    for project in projects:
        table.put_item(Item=project)
    
    print(f"✅ Populated {len(projects)} projects")

def populate_certifications(dynamodb, environment='dev'):
    """Populate certifications table with sample data"""
    table_name = get_table_name('certifications', environment)
    table = dynamodb.Table(table_name)
    
    certifications = [
        {
            'id': str(uuid.uuid4()),
            'name': 'AWS Certified Solutions Architect - Associate',
            'provider': 'Amazon Web Services',
            'issue_date': '2023-06-15',
            'expiry_date': '2026-06-15',
            'credential_id': 'AWS-SAA-2023-001234',
            'verification_url': 'https://aws.amazon.com/verification'
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'HashiCorp Certified: Terraform Associate',
            'provider': 'HashiCorp',
            'issue_date': '2023-08-20',
            'expiry_date': '2025-08-20',
            'credential_id': 'HC-TA-2023-005678'
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'GitHub Actions Certification',
            'provider': 'GitHub',
            'issue_date': '2023-10-10',
            'expiry_date': None,
            'credential_id': 'GH-AC-2023-009876'
        }
    ]
    
    for cert in certifications:
        table.put_item(Item=cert)
    
    print(f"✅ Populated {len(certifications)} certifications")

def populate_adrs(dynamodb, environment='dev'):
    """Populate ADRs table with sample data"""
    table_name = get_table_name('adrs', environment)
    table = dynamodb.Table(table_name)
    
    adrs = [
        {
            'id': 'ADR-001',
            'title': 'Use Serverless Architecture for CV API',
            'status': 'accepted',
            'date': '2024-01-01',
            'context': 'Need scalable, cost-effective API for CV data',
            'decision': 'Use AWS Lambda + API Gateway for serverless API',
            'consequences': 'Lower costs, automatic scaling, but cold start latency'
        },
        {
            'id': 'ADR-002',
            'title': 'Multi-Environment Strategy',
            'status': 'accepted',
            'date': '2024-01-05',
            'context': 'Need separate environments for development and production',
            'decision': 'Use Terraform workspaces with branch-based deployments',
            'consequences': 'Better isolation but more complex CI/CD'
        },
        {
            'id': 'ADR-003',
            'title': 'Private S3 with CloudFront OAC',
            'status': 'accepted',
            'date': '2024-01-10',
            'context': 'Security requirement for private S3 buckets',
            'decision': 'Use CloudFront with Origin Access Control instead of public S3',
            'consequences': 'Better security but more complex setup'
        }
    ]
    
    for adr in adrs:
        table.put_item(Item=adr)
    
    print(f"✅ Populated {len(adrs)} ADRs")

def populate_versions(dynamodb, environment='dev'):
    """Populate versions table with sample data"""
    table_name = get_table_name('versions', environment)
    table = dynamodb.Table(table_name)
    
    version = {
        'id': 'current',
        'version': '1.0.0',
        'release_date': datetime.now().isoformat(),
        'environment': environment,
        'git_commit': 'abc123def456',
        'features': [
            'Multi-environment infrastructure',
            'Serverless API endpoints',
            'Real-time CV data',
            'Interactive frontend'
        ]
    }
    
    table.put_item(Item=version)
    print(f"✅ Populated version info")

def main():
    """Main function to populate all tables"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Populate CV data')
    parser.add_argument('--environment', '-e', default='dev', 
                       help='Environment (dev, test, prod)')
    parser.add_argument('--region', '-r', default='us-east-1',
                       help='AWS region')
    
    args = parser.parse_args()
    
    # Initialize DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name=args.region)
    
    print(f"🚀 Populating CV data for {args.environment} environment...")
    
    try:
        populate_skills(dynamodb, args.environment)
        populate_projects(dynamodb, args.environment)
        populate_certifications(dynamodb, args.environment)
        populate_adrs(dynamodb, args.environment)
        populate_versions(dynamodb, args.environment)
        
        print(f"\n✅ Successfully populated all CV data for {args.environment}!")
        print(f"🌐 Your living CV is ready at: https://journey.oyintech.dev")
        
    except Exception as e:
        print(f"❌ Error populating data: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())