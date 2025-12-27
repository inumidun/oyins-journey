# Manual AWS Setup Guide

Since Terraform is blocked by network issues, let's create the resources manually in AWS Console.

## Step 1: Create DynamoDB Tables

### 1.1 Skills Table
1. Go to **DynamoDB Console** → **Create Table**
2. **Table name**: `oyins-journey-skills`
3. **Partition key**: `skill_id` (String)
4. **Settings**: On-demand billing
5. **Create Global Secondary Index**:
   - **Index name**: `CategoryIndex`
   - **Partition key**: `category` (String)
6. **Create Table**

### 1.2 Projects Table
1. **Table name**: `oyins-journey-projects`
2. **Partition key**: `project_id` (String)
3. **Settings**: On-demand billing
4. **Create Table**

### 1.3 Certifications Table
1. **Table name**: `oyins-journey-certifications`
2. **Partition key**: `cert_id` (String)
3. **Settings**: On-demand billing
4. **Create Global Secondary Index**:
   - **Index name**: `ProviderIndex`
   - **Partition key**: `provider` (String)
5. **Create Table**

### 1.4 ADRs Table
1. **Table name**: `oyins-journey-adrs`
2. **Partition key**: `adr_id` (String)
3. **Settings**: On-demand billing
4. **Create Table**

### 1.5 Versions Table
1. **Table name**: `oyins-journey-versions`
2. **Partition key**: `version_id` (String)
3. **Settings**: On-demand billing
4. **Create Table**

## Step 2: Create S3 Buckets

### 2.1 Frontend Bucket
1. Go to **S3 Console** → **Create Bucket**
2. **Bucket name**: `oyins-journey-frontend-[random-suffix]`
3. **Region**: us-east-1
4. **Uncheck "Block all public access"**
5. **Create Bucket**
6. **Properties** → **Static website hosting** → **Enable**
7. **Index document**: `index.html`
8. **Permissions** → **Bucket Policy**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::oyins-journey-frontend-[your-suffix]/*"
    }
  ]
}
```

### 2.2 Admin Bucket
1. **Bucket name**: `oyins-journey-admin-[random-suffix]`
2. Follow same steps as frontend bucket

## Step 3: Create IAM Role for Lambda

1. Go to **IAM Console** → **Roles** → **Create Role**
2. **Trusted entity**: AWS Service → Lambda
3. **Permissions**: Create custom policy:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Query",
        "dynamodb:Scan"
      ],
      "Resource": [
        "arn:aws:dynamodb:us-east-1:*:table/oyins-journey-*",
        "arn:aws:dynamodb:us-east-1:*:table/oyins-journey-*/index/*"
      ]
    }
  ]
}
```
4. **Role name**: `oyins-journey-lambda-role`

## Step 4: Create API Gateway

1. Go to **API Gateway Console** → **Create API**
2. **REST API** → **Build**
3. **API name**: `oyins-journey-api`
4. **Create API**

## Next Steps

After creating these resources manually:
1. Deploy Lambda functions
2. Configure API Gateway endpoints
3. Upload frontend files to S3
4. Test the system

This manual approach bypasses the Terraform network issues and gets us deployed faster.