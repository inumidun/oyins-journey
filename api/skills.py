import json
import boto3
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
# Use environment variable for table name (no hardcoded environment)
table_name = os.environ.get('SKILLS_TABLE', 'oyins-journey-skills')
skills_table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Parse query parameters
        query_params = event.get('queryStringParameters') or {}
        category = query_params.get('category')
        cloud = query_params.get('cloud')
        proficiency = query_params.get('proficiency')
        
        skills = []
        
        if category:
            # Query by category using GSI
            try:
                response = skills_table.query(
                    IndexName='CategoryIndex',
                    KeyConditionExpression=Key('category').eq(category)
                )
                skills = response['Items']
            except Exception as e:
                print(f"Error querying by category: {str(e)}")
                # Fallback to scan if GSI is not available
                response = skills_table.scan()
                all_skills = response['Items']
                skills = [skill for skill in all_skills if skill.get('category') == category]
        else:
            # Scan all skills
            response = skills_table.scan()
            skills = response['Items']
        
        # Apply additional filters
        if cloud:
            skills = [
                skill for skill in skills 
                if cloud.lower() in [tech.lower() for tech in skill.get('technologies', [])]
                or cloud.lower() in skill.get('name', '').lower()
                or cloud.lower() in skill.get('cloud', '').lower()
            ]
        
        if proficiency:
            skills = [
                skill for skill in skills 
                if skill.get('proficiency', '').lower() == proficiency.lower()
            ]
        
        # Sort skills by proficiency level and years of experience
        proficiency_order = {'expert': 4, 'advanced': 3, 'intermediate': 2, 'beginner': 1}
        skills.sort(
            key=lambda x: (
                proficiency_order.get(x.get('proficiency', '').lower(), 0),
                x.get('years_experience', 0)
            ),
            reverse=True
        )
        
        # Add computed fields for better frontend display
        for skill in skills:
            # Ensure all required fields exist
            skill.setdefault('proficiency', 'intermediate')
            skill.setdefault('years_experience', 0)
            skill.setdefault('technologies', [])
            skill.setdefault('category', 'other')
            
            # Add computed display fields
            skill['display_name'] = skill.get('name', skill.get('skill_id', 'Unknown'))
            skill['experience_level'] = f"{skill.get('years_experience', 0)} years"
            
            # Add evidence links if they exist
            if 'evidence_links' in skill:
                skill['has_evidence'] = len(skill['evidence_links']) > 0
            else:
                skill['has_evidence'] = False
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'skills': skills,
                'count': len(skills),
                'filters_applied': {
                    'category': category,
                    'cloud': cloud,
                    'proficiency': proficiency
                }
            })
        }
        
    except Exception as e:
        print(f"Error in skills handler: {str(e)}")
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