# Secure Deployment Guide

## Most Secure Approach: AWS Systems Manager Parameter Store

### Step 1: Store Credentials Securely in AWS Parameter Store

**NEVER hardcode credentials!** Instead, store them securely in AWS Systems Manager Parameter Store:

```bash
# Set your environment and email
ENVIRONMENT="dev"  # or "prod"
PROJECT_NAME="oyins-journey"
ADMIN_EMAIL="your-email@example.com"

# Store admin email (standard parameter)
aws ssm put-parameter \
  --name "/${PROJECT_NAME}-${ENVIRONMENT}/admin/email" \
  --value "${ADMIN_EMAIL}" \
  --type "String" \
  --description "Admin email for Cognito user pool"

# Store temporary password (encrypted parameter)
aws ssm put-parameter \
  --name "/${PROJECT_NAME}-${ENVIRONMENT}/admin/temp-password" \
  --value "YourSecurePassword123!" \
  --type "SecureString" \
  --description "Temporary password for admin user" \
  --key-id "alias/aws/ssm"
```

### Step 2: Deploy Infrastructure (Secure Mode)

```bash
cd infrastructure

# Initialize Terraform
terraform init

# Plan deployment (using SSM parameters by default)
terraform plan -var="environment=${ENVIRONMENT}"

# Apply deployment (no sensitive data in command line!)
terraform apply -var="environment=${ENVIRONMENT}"
```

### Step 3: Alternative - Environment-Specific tfvars Files

Create environment-specific variable files (add to .gitignore):

```bash
# Create terraform.tfvars (NEVER commit this file!)
cat > terraform.tfvars << EOF
environment = "dev"
admin_email = "your-email@example.com"
admin_temp_password = "YourSecurePassword123!"
use_ssm_password = false
EOF

# Add to .gitignore
echo "terraform.tfvars" >> .gitignore
echo "*.tfvars" >> .gitignore
```

Then deploy:
```bash
terraform apply
```

### Step 4: CI/CD Pipeline Approach (Most Secure for Production)

For production deployments, use GitHub Actions with encrypted secrets:

```yaml
# .github/workflows/deploy.yml
name: Deploy Infrastructure
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Store admin credentials in Parameter Store
        run: |
          aws ssm put-parameter \
            --name "/oyins-journey-prod/admin/email" \
            --value "${{ secrets.ADMIN_EMAIL }}" \
            --type "String" \
            --overwrite
          
          aws ssm put-parameter \
            --name "/oyins-journey-prod/admin/temp-password" \
            --value "${{ secrets.ADMIN_TEMP_PASSWORD }}" \
            --type "SecureString" \
            --overwrite
      
      - name: Deploy with Terraform
        run: |
          cd infrastructure
          terraform init
          terraform apply -auto-approve -var="environment=prod"
```

## Frontend Configuration

### Get Infrastructure Outputs

After deployment, get the required values:

```bash
terraform output api_gateway_url
terraform output cognito_user_pool_id
terraform output cognito_user_pool_client_id
```

### Configure Frontend Environment

Update `frontend/.env.development` with the actual values:

```env
VITE_API_URL=https://your-actual-api-gateway-url.execute-api.us-east-1.amazonaws.com/dev
VITE_COGNITO_USER_POOL_ID=us-east-1_XXXXXXXXX
VITE_COGNITO_USER_POOL_CLIENT_ID=your-client-id
```

### Build and Deploy Frontend

```bash
cd frontend
npm install
npm run build

# Deploy to S3 (replace with your bucket name from terraform output)
aws s3 sync dist/ s3://your-frontend-bucket-name --delete

# Invalidate CloudFront cache (replace with your distribution ID)
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"
```

## Security Best Practices Summary

### ✅ DO:
1. **Use AWS Parameter Store** for sensitive data (default configuration)
2. **Use environment-specific tfvars files** (add to .gitignore)
3. **Use CI/CD with encrypted secrets** for production
4. **Change temporary password immediately** after first login
5. **Enable MFA** on your AWS account
6. **Use least-privilege IAM policies**

### ❌ DON'T:
1. **Never hardcode credentials** in Terraform files
2. **Never commit .tfvars files** to version control
3. **Never pass sensitive data** via command line arguments
4. **Never store credentials** in plain text files
5. **Never use the same password** across environments

## Quick Start (Recommended)

```bash
# 1. Store credentials securely
aws ssm put-parameter --name "/oyins-journey-dev/admin/email" --value "your-email@example.com" --type "String"
aws ssm put-parameter --name "/oyins-journey-dev/admin/temp-password" --value "SecurePass123!" --type "SecureString"

# 2. Deploy infrastructure
cd infrastructure
terraform init
terraform apply -var="environment=dev"

# 3. Get outputs and configure frontend
terraform output api_gateway_url
terraform output cognito_user_pool_id
terraform output cognito_user_pool_client_id
```

## Admin Portal Setup

### 1. Initial Admin Login

1. Go to `https://your-domain.com/admin/login`
2. Use the email and temporary password you stored in Parameter Store
3. You'll be prompted to set a new password on first login

### 2. Configure Site Settings

1. Navigate to the Site Configuration section in the admin portal
2. Update your social links, branding, and site URLs
3. Save the configuration

### 3. Start Using Analytics

The analytics system will automatically start tracking page views once visitors access your site. View analytics in the admin portal.

## Troubleshooting

### Authentication Issues

- Ensure Cognito environment variables are correctly set
- Check that the User Pool and Client ID match your infrastructure
- Verify the admin user exists in the Cognito User Pool

### Parameter Store Issues

- Verify parameters exist: `aws ssm get-parameter --name "/oyins-journey-dev/admin/email"`
- Check IAM permissions for SSM access
- Ensure parameter names match the expected format

### API Issues

- Confirm the API Gateway URL is correct in environment variables
- Check that Lambda functions have proper DynamoDB permissions
- Verify CORS is configured correctly for your domain

This approach ensures:
- **No sensitive data in code or command history**
- **Encrypted storage of credentials**
- **Audit trail of parameter access**
- **Easy rotation of credentials**
- **Environment isolation**