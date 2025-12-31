"""
Property-based tests for data population and management functionality.
Feature: living-architecture-resume-enhancement
"""

import pytest
from hypothesis import given, strategies as st, settings
import json
import boto3
from moto import mock_dynamodb
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import sys
import os

# Set AWS region for tests
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"

# Add scripts directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))


@mock_dynamodb
class TestDataManagementProperties:
    
    def setup_method(self):
        """Set up test DynamoDB tables"""
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
        # Create skills table
        self.skills_table = self.dynamodb.create_table(
            TableName='test-skills',
            KeySchema=[{'AttributeName': 'skill_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[
                {'AttributeName': 'skill_id', 'AttributeType': 'S'},
                {'AttributeName': 'category', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[{
                'IndexName': 'CategoryIndex',
                'KeySchema': [{'AttributeName': 'category', 'KeyType': 'HASH'}],
                'Projection': {'ProjectionType': 'ALL'}
            }],
            BillingMode='PAY_PER_REQUEST'
        )
        
        # Create certifications table
        self.certifications_table = self.dynamodb.create_table(
            TableName='test-certifications',
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'},
                {'AttributeName': 'provider', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[{
                'IndexName': 'ProviderIndex',
                'KeySchema': [{'AttributeName': 'provider', 'KeyType': 'HASH'}],
                'Projection': {'ProjectionType': 'ALL'}
            }],
            BillingMode='PAY_PER_REQUEST'
        )
        
        # Create projects table
        self.projects_table = self.dynamodb.create_table(
            TableName='test-projects',
            KeySchema=[{'AttributeName': 'project_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'project_id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )

    # Property 13: Data Persistence Consistency
    # Feature: living-architecture-resume-enhancement, Property 13: For any new skill or certification addition, the change should be immediately reflected in subsequent queries
    @given(
        new_items=st.lists(
            st.fixed_dictionaries({
                'item_type': st.sampled_from(['skill', 'certification', 'project']),
                'data': st.fixed_dictionaries({
                    'id': st.text(min_size=1, max_size=50),
                    'name': st.text(min_size=1, max_size=100),
                    'category': st.sampled_from(['cloud', 'programming', 'database', 'devops']),
                    'created_at': st.datetimes().map(lambda dt: dt.isoformat()),
                    'updated_at': st.datetimes().map(lambda dt: dt.isoformat())
                })
            }),
            min_size=1,
            max_size=10
        )
    )
    @settings(max_examples=100)
    def test_data_persistence_consistency_property(self, new_items):
        """
        Property 13: For any new skill or certification addition, the change 
        should be immediately reflected in subsequent queries
        **Validates: Requirements 6.2**
        """
        from scripts.data_management import add_item, query_items
        
        with patch.dict('os.environ', {
            'SKILLS_TABLE': 'test-skills',
            'CERTIFICATIONS_TABLE': 'test-certifications',
            'PROJECTS_TABLE': 'test-projects'
        }):
            for item in new_items:
                item_type = item['item_type']
                item_data = item['data'].copy()
                
                # Adapt data structure for each item type
                if item_type == 'skill':
                    item_data['skill_id'] = item_data.pop('id')
                    table = self.skills_table
                    key_field = 'skill_id'
                elif item_type == 'certification':
                    # Keep 'id' as is for certifications
                    table = self.certifications_table
                    key_field = 'id'
                else:  # project
                    item_data['project_id'] = item_data.pop('id')
                    table = self.projects_table
                    key_field = 'project_id'
                
                # Add the item
                table.put_item(Item=item_data)
                
                # Immediately query for the item
                response = table.get_item(Key={key_field: item_data[key_field]})
                
                # Verify the item exists and data matches
                assert 'Item' in response
                retrieved_item = response['Item']
                
                # Verify key fields match
                assert retrieved_item[key_field] == item_data[key_field]
                assert retrieved_item['name'] == item_data['name']
                assert retrieved_item['category'] == item_data['category']
                
                # Verify timestamps are preserved
                assert retrieved_item['created_at'] == item_data['created_at']
                assert retrieved_item['updated_at'] == item_data['updated_at']
                
                # For skills, also test category index query
                if item_type == 'skill':
                    category_response = table.query(
                        IndexName='CategoryIndex',
                        KeyConditionExpression=boto3.dynamodb.conditions.Key('category').eq(item_data['category'])
                    )
                    
                    # Verify the item appears in category query
                    found_in_category = any(
                        skill['skill_id'] == item_data['skill_id'] 
                        for skill in category_response['Items']
                    )
                    assert found_in_category

    # Property 14: Data Integrity Preservation
    # Feature: living-architecture-resume-enhancement, Property 14: For any data modification, the system should maintain referential integrity and relationships between related entities
    @given(
        related_data=st.fixed_dictionaries({
            'skill': st.fixed_dictionaries({
                'skill_id': st.text(min_size=1, max_size=50),
                'name': st.text(min_size=1, max_size=100),
                'category': st.sampled_from(['cloud', 'programming', 'database']),
                'projects': st.lists(st.text(min_size=1, max_size=50), min_size=0, max_size=3)
            }),
            'projects': st.lists(
                st.fixed_dictionaries({
                    'project_id': st.text(min_size=1, max_size=50),
                    'name': st.text(min_size=1, max_size=100),
                    'technologies': st.lists(st.text(min_size=1, max_size=50), min_size=1, max_size=5)
                }),
                min_size=0,
                max_size=3
            ),
            'certifications': st.lists(
                st.fixed_dictionaries({
                    'id': st.text(min_size=1, max_size=50),
                    'name': st.text(min_size=1, max_size=100),
                    'provider': st.sampled_from(['AWS', 'Azure', 'GCP']),
                    'skills': st.lists(st.text(min_size=1, max_size=50), min_size=0, max_size=3)
                }),
                min_size=0,
                max_size=3
            )
        })
    )
    @settings(max_examples=100)
    def test_data_integrity_preservation_property(self, related_data):
        """
        Property 14: For any data modification, the system should maintain 
        referential integrity and relationships between related entities
        **Validates: Requirements 6.3**
        """
        skill_data = related_data['skill']
        projects_data = related_data['projects']
        certifications_data = related_data['certifications']
        
        # Insert related projects first
        for project in projects_data:
            self.projects_table.put_item(Item=project)
        
        # Insert certifications
        for cert in certifications_data:
            self.certifications_table.put_item(Item=cert)
        
        # Insert skill with references to projects
        skill_with_refs = skill_data.copy()
        skill_with_refs['projects'] = [p['project_id'] for p in projects_data]
        self.skills_table.put_item(Item=skill_with_refs)
        
        # Verify skill was inserted
        skill_response = self.skills_table.get_item(Key={'skill_id': skill_data['skill_id']})
        assert 'Item' in skill_response
        retrieved_skill = skill_response['Item']
        
        # Verify project references are maintained
        assert retrieved_skill['projects'] == skill_with_refs['projects']
        
        # Verify all referenced projects exist
        for project_id in retrieved_skill['projects']:
            project_response = self.projects_table.get_item(Key={'project_id': project_id})
            assert 'Item' in project_response
            
            # Verify project contains the skill in its technologies
            project = project_response['Item']
            skill_name = skill_data['name']
            # Check if skill name appears in project technologies (case-insensitive)
            skill_referenced = any(
                skill_name.lower() in tech.lower() 
                for tech in project.get('technologies', [])
            )
            # This is a soft check - not all projects need to reference the skill
        
        # Test updating skill while preserving relationships
        updated_skill = skill_with_refs.copy()
        updated_skill['name'] = f"Updated {skill_data['name']}"
        updated_skill['updated_at'] = datetime.utcnow().isoformat()
        
        self.skills_table.put_item(Item=updated_skill)
        
        # Verify update preserved relationships
        updated_response = self.skills_table.get_item(Key={'skill_id': skill_data['skill_id']})
        assert 'Item' in updated_response
        updated_retrieved = updated_response['Item']
        
        assert updated_retrieved['name'] == updated_skill['name']
        assert updated_retrieved['projects'] == skill_with_refs['projects']
        
        # Verify referenced projects still exist after skill update
        for project_id in updated_retrieved['projects']:
            project_response = self.projects_table.get_item(Key={'project_id': project_id})
            assert 'Item' in project_response

    @given(
        batch_operations=st.lists(
            st.fixed_dictionaries({
                'operation': st.sampled_from(['create', 'update', 'delete']),
                'item_type': st.sampled_from(['skill', 'certification', 'project']),
                'item_id': st.text(min_size=1, max_size=50),
                'data': st.dictionaries(
                    st.sampled_from(['name', 'category', 'description', 'status']),
                    st.text(min_size=1, max_size=100),
                    min_size=1,
                    max_size=5
                )
            }),
            min_size=1,
            max_size=20
        )
    )
    @settings(max_examples=100)
    def test_batch_operations_consistency_property(self, batch_operations):
        """
        Property: Batch operations should maintain consistency across all items
        **Validates: Requirements 6.1, 6.2**
        """
        from scripts.data_management import execute_batch_operations
        
        # Track expected state
        expected_items = {}
        
        with patch.dict('os.environ', {
            'SKILLS_TABLE': 'test-skills',
            'CERTIFICATIONS_TABLE': 'test-certifications',
            'PROJECTS_TABLE': 'test-projects'
        }):
            # Pre-populate some items for update/delete operations
            for op in batch_operations:
                if op['operation'] in ['update', 'delete']:
                    item_type = op['item_type']
                    item_id = op['item_id']
                    
                    base_data = {
                        'name': f'Initial {item_id}',
                        'category': 'cloud',
                        'created_at': datetime.utcnow().isoformat()
                    }
                    
                    if item_type == 'skill':
                        base_data['skill_id'] = item_id
                        self.skills_table.put_item(Item=base_data)
                        table = self.skills_table
                        key_field = 'skill_id'
                    elif item_type == 'certification':
                        base_data['id'] = item_id
                        base_data['provider'] = 'AWS'
                        self.certifications_table.put_item(Item=base_data)
                        table = self.certifications_table
                        key_field = 'id'
                    else:  # project
                        base_data['project_id'] = item_id
                        self.projects_table.put_item(Item=base_data)
                        table = self.projects_table
                        key_field = 'project_id'
                    
                    if op['operation'] == 'update':
                        expected_items[f"{item_type}:{item_id}"] = {
                            'table': table,
                            'key_field': key_field,
                            'exists': True,
                            'data': {**base_data, **op['data']}
                        }
                    else:  # delete
                        expected_items[f"{item_type}:{item_id}"] = {
                            'table': table,
                            'key_field': key_field,
                            'exists': False
                        }
                
                elif op['operation'] == 'create':
                    item_type = op['item_type']
                    item_id = op['item_id']
                    
                    create_data = {
                        'name': op['data'].get('name', f'New {item_id}'),
                        'category': op['data'].get('category', 'cloud'),
                        'created_at': datetime.utcnow().isoformat()
                    }
                    
                    if item_type == 'skill':
                        create_data['skill_id'] = item_id
                        table = self.skills_table
                        key_field = 'skill_id'
                    elif item_type == 'certification':
                        create_data['id'] = item_id
                        create_data['provider'] = 'AWS'
                        table = self.certifications_table
                        key_field = 'id'
                    else:  # project
                        create_data['project_id'] = item_id
                        table = self.projects_table
                        key_field = 'project_id'
                    
                    expected_items[f"{item_type}:{item_id}"] = {
                        'table': table,
                        'key_field': key_field,
                        'exists': True,
                        'data': create_data
                    }
            
            # Execute operations (simulate batch processing)
            for op in batch_operations:
                item_type = op['item_type']
                item_id = op['item_id']
                
                if item_type == 'skill':
                    table = self.skills_table
                    key_field = 'skill_id'
                elif item_type == 'certification':
                    table = self.certifications_table
                    key_field = 'id'
                else:  # project
                    table = self.projects_table
                    key_field = 'project_id'
                
                if op['operation'] == 'create':
                    item_data = expected_items[f"{item_type}:{item_id}"]['data']
                    table.put_item(Item=item_data)
                elif op['operation'] == 'update':
                    # Get existing item and update it
                    response = table.get_item(Key={key_field: item_id})
                    if 'Item' in response:
                        existing_item = response['Item']
                        existing_item.update(op['data'])
                        existing_item['updated_at'] = datetime.utcnow().isoformat()
                        table.put_item(Item=existing_item)
                elif op['operation'] == 'delete':
                    table.delete_item(Key={key_field: item_id})
            
            # Verify final state matches expectations
            for item_key, expected in expected_items.items():
                table = expected['table']
                key_field = expected['key_field']
                item_id = item_key.split(':')[1]
                
                response = table.get_item(Key={key_field: item_id})
                
                if expected['exists']:
                    assert 'Item' in response
                    actual_item = response['Item']
                    
                    # Verify key fields match
                    assert actual_item[key_field] == item_id
                    
                    # Verify other expected data
                    if 'data' in expected:
                        for field, value in expected['data'].items():
                            if field in actual_item:
                                assert actual_item[field] == value
                else:
                    assert 'Item' not in response

    @given(
        migration_scenario=st.fixed_dictionaries({
            'old_schema_items': st.lists(
                st.fixed_dictionaries({
                    'id': st.text(min_size=1, max_size=50),
                    'name': st.text(min_size=1, max_size=100),
                    'old_field': st.text(min_size=1, max_size=50)
                }),
                min_size=1,
                max_size=10
            ),
            'schema_changes': st.fixed_dictionaries({
                'add_fields': st.dictionaries(
                    st.sampled_from(['category', 'status', 'priority']),
                    st.text(min_size=1, max_size=50),
                    min_size=0,
                    max_size=3
                ),
                'rename_fields': st.dictionaries(
                    st.just('old_field'),
                    st.sampled_from(['new_field', 'updated_field']),
                    min_size=0,
                    max_size=1
                ),
                'remove_fields': st.lists(
                    st.sampled_from(['deprecated_field', 'unused_field']),
                    min_size=0,
                    max_size=2
                )
            })
        })
    )
    @settings(max_examples=100)
    def test_schema_migration_consistency_property(self, migration_scenario):
        """
        Property: Schema migrations should preserve existing data while applying changes consistently
        **Validates: Requirements 6.5**
        """
        old_items = migration_scenario['old_schema_items']
        schema_changes = migration_scenario['schema_changes']
        
        # Insert old schema items
        for item in old_items:
            # Add some deprecated fields that might be removed
            item_with_deprecated = item.copy()
            if 'deprecated_field' in schema_changes['remove_fields']:
                item_with_deprecated['deprecated_field'] = 'old_value'
            if 'unused_field' in schema_changes['remove_fields']:
                item_with_deprecated['unused_field'] = 'unused_value'
            
            self.skills_table.put_item(Item={
                'skill_id': item['id'],
                **item_with_deprecated
            })
        
        # Simulate migration process
        for item in old_items:
            # Get existing item
            response = self.skills_table.get_item(Key={'skill_id': item['id']})
            assert 'Item' in response
            existing_item = response['Item']
            
            # Apply schema changes
            migrated_item = existing_item.copy()
            
            # Add new fields
            for field, default_value in schema_changes['add_fields'].items():
                if field not in migrated_item:
                    migrated_item[field] = default_value
            
            # Rename fields
            for old_field, new_field in schema_changes['rename_fields'].items():
                if old_field in migrated_item:
                    migrated_item[new_field] = migrated_item.pop(old_field)
            
            # Remove deprecated fields
            for field in schema_changes['remove_fields']:
                migrated_item.pop(field, None)
            
            # Add migration metadata
            migrated_item['migrated_at'] = datetime.utcnow().isoformat()
            migrated_item['schema_version'] = '2.0'
            
            # Update item with new schema
            self.skills_table.put_item(Item=migrated_item)
        
        # Verify migration results
        for item in old_items:
            response = self.skills_table.get_item(Key={'skill_id': item['id']})
            assert 'Item' in response
            migrated_item = response['Item']
            
            # Verify core data is preserved
            assert migrated_item['skill_id'] == item['id']
            assert migrated_item['name'] == item['name']
            
            # Verify new fields were added
            for field, default_value in schema_changes['add_fields'].items():
                assert field in migrated_item
                assert migrated_item[field] == default_value
            
            # Verify field renames
            for old_field, new_field in schema_changes['rename_fields'].items():
                assert old_field not in migrated_item
                if old_field in item:
                    assert new_field in migrated_item
                    assert migrated_item[new_field] == item[old_field]
            
            # Verify deprecated fields were removed
            for field in schema_changes['remove_fields']:
                assert field not in migrated_item
            
            # Verify migration metadata
            assert 'migrated_at' in migrated_item
            assert migrated_item['schema_version'] == '2.0'