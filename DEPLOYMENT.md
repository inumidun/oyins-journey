# Deployment Guide

## Prerequisites

1. AWS CLI configured with appropriate permissions
2. Terraform installed (>= 1.0)
3. Node.js and npm installed

## Infrastructure Deployment

### 1. Deploy Infrastructure with Cognito

```bash
cd infrastructure
terraform init
terraform plan -var="environment=dev" -var="admin_email=your-email@example.com" -var="admin_temp_password=TempPassword123!"
terraform apply -var="environment=dev" -var="admin_email=your-email@example.com" -var="admin_temp_password=TempPassword123!"
```

### 2. Get Infrastructure Outputs

After deployment, get the required values:

```bash
terraform output api_gateway_url
terraform output cognito_user_pool_id
terraform output cognito_user_pool_client_id
```

### 3. Configure Frontend Environment

Update `frontend/.env.development` with the actual values:

```env
VITE_API_URL=https://your-actual-api-gateway-url.execute-api.us-east-1.amazonaws.com/dev
VITE_COGNITO_USER_POOL_ID=us-east-1_XXXXXXXXX
VITE_COGNITO_USER_POOL_CLIENT_ID=your-client-id
```

### 4. Build and Deploy Frontend

```bash
cd frontend
npm install
npm run build

# Deploy to S3 (replace with your bucket name from terraform output)
aws s3 sync dist/ s3://your-frontend-bucket-name --delete

# Invalidate CloudFront cache (replace with your distribution ID)
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"
```

## Admin Portal Setup

### 1. Initial Admin Login

1. Go to `https://your-domain.com/admin/login`
2. Use the email and temporary password you set during infrastructure deployment
3. You'll be prompted to set a new password on first login

### 2. Configure Site Settings

1. Navigate to the Site Configuration section in the admin portal
2. Update your social links, branding, and site URLs
3. Save the configuration

### 3. Start Using Analytics

The analytics system will automatically start tracking page views once visitors access your site. View analytics in the admin portal.

## Environment Variables

### Required for Infrastructure

- `admin_email`: Your admin email address for Cognito user
- `admin_temp_password`: Temporary password (must meet AWS password requirements)
- `environment`: Deployment environment (dev, test, prod)

### Required for Frontend

- `VITE_API_URL`: API Gateway URL from Terraform output
- `VITE_COGNITO_USER_POOL_ID`: Cognito User Pool ID from Terraform output
- `VITE_COGNITO_USER_POOL_CLIENT_ID`: Cognito User Pool Client ID from Terraform output

## Security Notes

1. **Change the temporary password immediately** after first login
2. The Cognito User Pool is configured with strong password requirements
3. Admin API endpoints are protected with Cognito JWT tokens
4. Analytics data is stored locally and contains no PII
5. All social links and URLs are validated before saving

## Troubleshooting

### Authentication Issues

- Ensure Cognito environment variables are correctly set
- Check that the User Pool and Client ID match your infrastructure
- Verify the admin user exists in the Cognito User Pool

### API Issues

- Confirm the API Gateway URL is correct in environment variables
- Check that Lambda functions have proper DynamoDB permissions
- Verify CORS is configured correctly for your domain

### Build Issues

- Run `npm install` to ensure all dependencies are installed
- Check TypeScript compilation with `npm run build`
- Verify all UI components are properly imported

## Cost Optimization

- Cognito: First 50,000 MAUs are free, then $0.0055 per MAU
- DynamoDB: On-demand pricing for low-traffic sites
- Lambda: Pay per request, very cost-effective for portfolio sites
- S3 + CloudFront: Minimal costs for static site hosting

## Next Steps

After deployment, you can:

1. Add content management forms for projects, skills, and certifications
2. Implement server-side analytics with CloudWatch
3. Add more authentication providers (Google, GitHub, etc.)
4. Set up automated backups for DynamoDB data
5. Configure custom domain with SSL certificate