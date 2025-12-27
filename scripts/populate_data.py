import boto3
import json
from datetime import datetime

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def populate_skills():
    table = dynamodb.Table('oyins-journey-skills')
    
    skills = [
        {
            'skill_id': 'aws-lambda',
            'name': 'AWS Lambda',
            'category': 'cloud',
            'proficiency': 'advanced',
            'technologies': ['Python', 'Node.js', 'Serverless'],
            'evidence_links': [
                'https://github.com/your-repo/lambda-project',
                'https://your-api.amazonaws.com/skills'
            ],
            'usage_count': 15
        },
        {
            'skill_id': 'terraform',
            'name': 'Terraform',
            'category': 'devops',
            'proficiency': 'advanced',
            'technologies': ['IaC', 'AWS', 'Infrastructure'],
            'evidence_links': [
                'https://github.com/your-repo/terraform-modules'
            ],
            'usage_count': 8
        },
        {
            'skill_id': 'dynamodb',
            'name': 'DynamoDB',
            'category': 'database',
            'proficiency': 'intermediate',
            'technologies': ['NoSQL', 'AWS', 'Serverless'],
            'evidence_links': [
                'https://your-api.amazonaws.com/projects'
            ],
            'usage_count': 5
        }
    ]
    
    for skill in skills:
        table.put_item(Item=skill)
    print(f"Added {len(skills)} skills")

def populate_projects():
    table = dynamodb.Table('oyins-journey-projects')
    
    projects = [
        {
            'project_id': 'living-architecture-resume',
            'name': 'Living Architecture Resume',
            'description': 'A self-documenting, queryable cloud architecture that serves as a CV',
            'technologies': ['AWS Lambda', 'DynamoDB', 'API Gateway', 'Terraform', 'S3'],
            'start_date': '2024-01-01',
            'status': 'active',
            'github_url': 'https://github.com/your-username/living-architecture-resume',
            'live_url': 'https://your-resume.s3-website.amazonaws.com',
            'architecture_decisions': ['lambda-over-ec2', 'dynamodb-over-rds']
        }
    ]
    
    for project in projects:
        table.put_item(Item=project)
    print(f"Added {len(projects)} projects")

def populate_adrs():
    table = dynamodb.Table('oyins-journey-adrs')
    
    adrs = [
        {
            'adr_id': 'adr-001',
            'title': 'Use Lambda over EC2',
            'decision': 'Lambda over EC2',
            'context': 'Need serverless compute for API endpoints',
            'options_considered': ['EC2', 'Lambda', 'Fargate'],
            'decision_rationale': 'Free-tier friendly, zero maintenance, auto-scaling',
            'tradeoffs': ['Cold starts', 'Execution time limits', 'Memory constraints'],
            'aws_services': ['Lambda', 'API Gateway'],
            'date': '2024-01-01',
            'status': 'accepted'
        },
        {
            'adr_id': 'adr-002',
            'title': 'Use DynamoDB over RDS',
            'decision': 'DynamoDB over RDS',
            'context': 'Need database for CV data storage',
            'options_considered': ['RDS PostgreSQL', 'DynamoDB', 'Aurora Serverless'],
            'decision_rationale': 'Serverless, pay-per-request, fits data model',
            'tradeoffs': ['Limited query flexibility', 'Learning curve'],
            'aws_services': ['DynamoDB'],
            'date': '2024-01-02',
            'status': 'accepted'
        }
    ]
    
    for adr in adrs:
        table.put_item(Item=adr)
    print(f"Added {len(adrs)} ADRs")

def populate_versions():
    table = dynamodb.Table('oyins-journey-versions')
    
    versions = [
        {
            'version_id': 'v1.0.0',
            'version': '1.0.0',
            'release_date': datetime.now().isoformat(),
            'features': [
                'Initial serverless architecture',
                'Skills API endpoint',
                'Projects API endpoint',
                'Certifications API endpoint',
                'Architecture Decision Records',
                'Basic frontend'
            ],
            'deployment_count': 1,
            'infrastructure_changes': [
                'Created DynamoDB tables',
                'Set up API Gateway',
                'Deployed Lambda functions'
            ]
        }
    ]
    
    for version in versions:
        table.put_item(Item=version)
    print(f"Added {len(versions)} versions")

def populate_certifications():
    table = dynamodb.Table('oyins-journey-certifications')
    
    certifications = [
        {
            'cert_id': 'aws-saa-c03',
            'name': 'AWS Certified Solutions Architect - Associate',
            'provider': 'aws',
            'earned_date': '2024-01-15',
            'expiry_date': '2027-01-15',
            'status': 'active',
            'credential_id': 'ABC123DEF456',
            'verification_url': 'https://aws.amazon.com/verification/ABC123DEF456',
            'skills_demonstrated': ['Cloud Architecture', 'AWS Services', 'Security', 'Cost Optimization']
        },
        {
            'cert_id': 'terraform-associate',
            'name': 'HashiCorp Certified: Terraform Associate',
            'provider': 'hashicorp',
            'earned_date': '2023-11-20',
            'expiry_date': '2025-11-20',
            'status': 'active',
            'credential_id': 'TERRA789XYZ',
            'verification_url': 'https://hashicorp.com/certification/verify/TERRA789XYZ',
            'skills_demonstrated': ['Infrastructure as Code', 'Terraform', 'Cloud Provisioning']
        }
    ]
    
    for cert in certifications:
        table.put_item(Item=cert)
    print(f"Added {len(certifications)} certifications")

if __name__ == '__main__':
    print("Populating Oyin's Journey data...")
    populate_skills()
    populate_projects()
    populate_adrs()
    populate_versions()
    populate_certifications()
    print("Data population complete!")