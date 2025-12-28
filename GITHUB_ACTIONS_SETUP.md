# GitHub Actions Setup Guide - Multi-Environment

## 🚀 **Step-by-Step GitHub Actions Deployment**

### **Step 1: Create GitHub Repository**
1. Go to GitHub.com
2. Create new repository: `oyins-journey`
3. Make it **public** (for free GitHub Actions)
4. Don't initialize with README (we have files already)

### **Step 2: Add AWS Credentials to GitHub Secrets**
1. Go to your repository → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add these secrets:

**Required Secrets:**
- `AWS_ACCESS_KEY_ID` = Your AWS access key
- `AWS_SECRET_ACCESS_KEY` = Your AWS secret key

### **Step 3: Set Up Branches and Push Code**
```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Oyin's Journey - Living Architecture Resume"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/oyins-journey.git

# Push to main branch
git push -u origin main

# Create and switch to dev branch
git checkout -b dev
git push -u origin dev

# Create test branch
git checkout main
git checkout -b test
git push -u origin test

# Switch back to dev for development
git checkout dev
```

### **Step 4: GitHub Actions Will Automatically Deploy:**

#### **Dev Environment** (on push to `dev` branch)
✅ **Terraform workspace**: `dev`
✅ **Resources**: `oyins-journey-dev-*`
✅ **S3 buckets**: `oyins-journey-dev-frontend-*`, `oyins-journey-dev-admin-*`
✅ **DynamoDB tables**: `oyins-journey-dev-skills`, etc.

#### **Test Environment** (on push to `test` branch)
✅ **Terraform workspace**: `test`
✅ **Resources**: `oyins-journey-test-*`
✅ **Isolated from dev environment**

#### **Production Environment** (on push to `main` branch)
✅ **Terraform workspace**: `default`
✅ **Resources**: `oyins-journey-prod-*`
✅ **Production-ready deployment**

### **Step 5: Monitor Deployment**
1. Go to **Actions** tab in your GitHub repository
2. Watch the deployment progress for each environment
3. Check for any errors in the logs
4. Each branch deploys to its own isolated environment

## 🔧 **Current Workflow Features**

Our `.github/workflows/deploy.yml` includes:
- ✅ **Multi-environment support** (dev/test/prod)
- ✅ **Terraform workspaces** for isolation
- ✅ **Environment-specific resource naming**
- ✅ **Lambda function packaging**
- ✅ **S3 frontend deployment**
- ✅ **S3 admin deployment**
- ✅ **Automatic version updates**

## 🎯 **Expected Results After Deployment**

### **Dev Environment** (`dev` branch)
- **DynamoDB tables**: `oyins-journey-dev-skills`, `oyins-journey-dev-projects`, etc.
- **S3 buckets**: `oyins-journey-dev-frontend-*`, `oyins-journey-dev-admin-*`
- **API Gateway**: `oyins-journey-dev-api`
- **IAM roles**: `oyins-journey-dev-lambda-role`

### **Test Environment** (`test` branch)
- **DynamoDB tables**: `oyins-journey-test-skills`, `oyins-journey-test-projects`, etc.
- **S3 buckets**: `oyins-journey-test-frontend-*`, `oyins-journey-test-admin-*`
- **API Gateway**: `oyins-journey-test-api`
- **IAM roles**: `oyins-journey-test-lambda-role`

### **Production Environment** (`main` branch)
- **DynamoDB tables**: `oyins-journey-prod-skills`, `oyins-journey-prod-projects`, etc.
- **S3 buckets**: `oyins-journey-prod-frontend-*`, `oyins-journey-prod-admin-*`
- **API Gateway**: `oyins-journey-prod-api`
- **IAM roles**: `oyins-journey-prod-lambda-role`

## 🔍 **Troubleshooting**

**If deployment fails:**
1. Check **Actions** tab for error logs
2. Verify AWS credentials in **Secrets**
3. Ensure AWS account has proper permissions
4. Check Terraform syntax in `infrastructure/main.tf`

## 📋 **Next Steps After Successful Deployment**

1. **Get S3 URLs** from GitHub Actions output
2. **Create Lambda functions** in AWS Console
3. **Populate sample data** using `scripts/populate_data.py`
4. **Test all endpoints**
5. **Set up custom domain** (optional)

---

**Ready to deploy? Follow the steps above and push to GitHub!**