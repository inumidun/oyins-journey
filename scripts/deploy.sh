#!/bin/bash

echo "🚀 Deploying Oyin's Journey..."

# Check if AWS CLI is configured
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "❌ AWS CLI not configured. Please run 'aws configure' first."
    exit 1
fi

# Deploy infrastructure
echo "📦 Deploying infrastructure with Terraform..."
cd infrastructure
terraform init
terraform plan
terraform apply -auto-approve

# Get outputs
S3_BUCKET=$(terraform output -raw s3_bucket_name)
API_URL=$(terraform output -raw api_gateway_url)

echo "✅ Infrastructure deployed!"
echo "📊 S3 Bucket: $S3_BUCKET"
echo "🔗 API URL: $API_URL"

# Deploy frontend
echo "🌐 Deploying frontend to S3..."
cd ../frontend
aws s3 sync . s3://$S3_BUCKET --delete

# Populate sample data
echo "📝 Populating sample data..."
cd ../scripts
python populate_data.py

echo "🎉 Oyin's Journey deployed successfully!"
echo "🌍 Frontend URL: http://$S3_BUCKET.s3-website-us-east-1.amazonaws.com"