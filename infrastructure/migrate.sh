#!/bin/bash
# Migration script to move from workspace-based to environment-specific remote state
# Run this ONCE per environment to migrate existing state

set -e

ENVIRONMENT=${1:-dev}
echo "🔄 Migrating $ENVIRONMENT state to remote backend..."

# Ensure backend exists
./bootstrap.sh

# Initialize with new backend
terraform init -backend-config="key=infrastructure/$ENVIRONMENT/terraform.tfstate" -migrate-state -force-copy

echo "✅ Migration complete for $ENVIRONMENT environment"