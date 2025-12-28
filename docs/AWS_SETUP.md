# AWS Setup Guide

## Step 1: Configure AWS CLI

You need to configure AWS CLI with your credentials before deploying.

### Option A: Using AWS Configure (Recommended)
```bash
aws configure
```

You'll be prompted for:
- **AWS Access Key ID**: Your access key
- **AWS Secret Access Key**: Your secret key  
- **Default region**: `us-east-1` (recommended)
- **Default output format**: `json`

### Option B: Using Environment Variables
```bash
set AWS_ACCESS_KEY_ID=your-access-key
set AWS_SECRET_ACCESS_KEY=your-secret-key
set AWS_DEFAULT_REGION=us-east-1
```

## Step 2: Verify Configuration
```bash
aws sts get-caller-identity
```

Should return your account information.

## Step 3: Deploy Infrastructure
```bash
cd infrastructure
terraform init
terraform plan
terraform apply
```

## Getting AWS Credentials

If you don't have AWS credentials:

1. **Sign in to AWS Console**
2. **Go to IAM** → Users → Your User
3. **Security Credentials** tab
4. **Create Access Key** → Command Line Interface (CLI)
5. **Download** the credentials

### Required Permissions
Your user needs these permissions:
- DynamoDB (CreateTable, PutItem, GetItem, Query, Scan)
- S3 (CreateBucket, PutObject, GetObject, PutBucketPolicy)
- IAM (CreateRole, AttachRolePolicy)
- API Gateway (CreateRestApi, CreateResource, CreateMethod)
- Lambda (CreateFunction, UpdateFunctionCode)

## Next Steps
Once AWS CLI is configured, run:
```bash
# Test connection
aws sts get-caller-identity

# Deploy infrastructure
cd infrastructure
terraform init
terraform apply
```