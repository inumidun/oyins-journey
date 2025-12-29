#!/bin/bash

# Frontend Build and Deploy Script
set -e

ENVIRONMENT=${1:-dev}
echo "🚀 Building frontend for $ENVIRONMENT environment..."

# Get API URL from Terraform output
cd ../infrastructure
API_URL=$(terraform output -raw api_gateway_url 2>/dev/null || echo "")

if [ -z "$API_URL" ]; then
    echo "⚠️  Warning: Could not get API URL from Terraform. Using default."
    API_URL="https://your-api-gateway-url.execute-api.us-east-1.amazonaws.com/$ENVIRONMENT"
fi

echo "📡 API URL: $API_URL"

# Build React app with API URL
cd ../frontend
export VITE_API_URL=$API_URL
export VITE_ENVIRONMENT=$ENVIRONMENT

echo "📦 Installing dependencies..."
npm install

echo "🔨 Building React application..."
npm run build

echo "📤 Deploying to S3..."
S3_BUCKET=$(cd ../infrastructure && terraform output -raw s3_bucket_name 2>/dev/null || echo "")
CLOUDFRONT_ID=$(cd ../infrastructure && terraform output -raw cloudfront_frontend_id 2>/dev/null || echo "")

if [ -n "$S3_BUCKET" ]; then
    aws s3 sync dist/ s3://$S3_BUCKET --delete
    echo "✅ Deployed to S3: $S3_BUCKET"
    
    if [ -n "$CLOUDFRONT_ID" ]; then
        echo "🔄 Invalidating CloudFront cache..."
        aws cloudfront create-invalidation --distribution-id $CLOUDFRONT_ID --paths "/*"
        echo "✅ CloudFront cache invalidated"
    fi
else
    echo "❌ Could not get S3 bucket name from Terraform"
    exit 1
fi

echo "🎉 Frontend deployment complete!"
echo "🌐 Your living CV is available at: https://$(cd ../infrastructure && terraform output -raw cloudfront_frontend_url 2>/dev/null || echo 'your-domain.com')"