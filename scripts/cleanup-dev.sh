#!/bin/bash

# Cleanup script for Oyin's Journey - Dev Environment
echo "🧹 Cleaning up existing AWS resources for dev environment..."

# Set AWS region
export AWS_DEFAULT_REGION=us-east-1

# Delete DynamoDB Tables
echo "Deleting DynamoDB tables..."
aws dynamodb delete-table --table-name oyins-journey-dev-skills || true
aws dynamodb delete-table --table-name oyins-journey-dev-projects || true
aws dynamodb delete-table --table-name oyins-journey-dev-adrs || true
aws dynamodb delete-table --table-name oyins-journey-dev-versions || true
aws dynamodb delete-table --table-name oyins-journey-dev-certifications || true

# Delete IAM Role and Policy
echo "Deleting IAM resources..."
aws iam delete-role-policy --role-name oyins-journey-dev-lambda-role --policy-name oyins-journey-dev-lambda-policy || true
aws iam delete-role --role-name oyins-journey-dev-lambda-role || true

# Delete API Gateway (if exists)
echo "Deleting API Gateway..."
API_ID=$(aws apigateway get-rest-apis --query "items[?name=='oyins-journey-dev-api'].id" --output text)
if [ "$API_ID" != "" ] && [ "$API_ID" != "None" ]; then
    aws apigateway delete-rest-api --rest-api-id $API_ID
    echo "Deleted API Gateway: $API_ID"
fi

# Delete S3 Buckets (empty first, then delete)
echo "Deleting S3 buckets..."
for bucket in $(aws s3 ls | grep "oyins-journey-dev-" | awk '{print $3}'); do
    echo "Emptying and deleting bucket: $bucket"
    aws s3 rm s3://$bucket --recursive || true
    aws s3 rb s3://$bucket || true
done

# Delete CloudFront Distributions (if any)
echo "Checking for CloudFront distributions..."
DISTRIBUTIONS=$(aws cloudfront list-distributions --query "DistributionList.Items[?contains(Comment, 'oyins-journey-dev')].Id" --output text)
for dist_id in $DISTRIBUTIONS; do
    if [ "$dist_id" != "" ] && [ "$dist_id" != "None" ]; then
        echo "Found CloudFront distribution: $dist_id"
        echo "Note: CloudFront distributions must be disabled before deletion"
        echo "Please disable manually in AWS Console, then delete"
    fi
done

echo "✅ Cleanup complete! You can now deploy with a clean slate."