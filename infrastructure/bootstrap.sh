#!/bin/bash
# Bootstrap script to create Terraform state backend
# Run this ONCE before any Terraform deployments

set -e

BUCKET_NAME="oyins-journey-terraform-state"
TABLE_NAME="oyins-journey-terraform-locks"
REGION="us-east-1"

echo "🚀 Creating Terraform state backend..."

# Create S3 bucket for state
aws s3api create-bucket --bucket $BUCKET_NAME --region $REGION 2>/dev/null || echo "Bucket already exists"

# Enable versioning
aws s3api put-bucket-versioning --bucket $BUCKET_NAME --versioning-configuration Status=Enabled

# Enable encryption
aws s3api put-bucket-encryption --bucket $BUCKET_NAME --server-side-encryption-configuration '{
  "Rules": [{
    "ApplyServerSideEncryptionByDefault": {
      "SSEAlgorithm": "AES256"
    }
  }]
}'

# Block public access
aws s3api put-public-access-block --bucket $BUCKET_NAME --public-access-block-configuration '{
  "BlockPublicAcls": true,
  "IgnorePublicAcls": true,
  "BlockPublicPolicy": true,
  "RestrictPublicBuckets": true
}'

# Create DynamoDB table for locks
aws dynamodb create-table \
  --table-name $TABLE_NAME \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region $REGION 2>/dev/null || echo "Table already exists"

echo "✅ Backend created: s3://$BUCKET_NAME with locks in $TABLE_NAME"