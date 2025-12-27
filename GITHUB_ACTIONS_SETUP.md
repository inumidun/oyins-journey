# GitHub Actions Setup Guide

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

### **Step 3: Push Code to GitHub**
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
```

### **Step 4: GitHub Actions Will Automatically:**
✅ **Trigger on push to main branch**
✅ **Deploy Terraform infrastructure**
✅ **Package Lambda functions**
✅ **Deploy frontend to S3**
✅ **Deploy admin interface to S3**

### **Step 5: Monitor Deployment**
1. Go to **Actions** tab in your GitHub repository
2. Watch the deployment progress
3. Check for any errors in the logs

## 🔧 **Current Workflow Features**

Our `.github/workflows/deploy.yml` includes:
- ✅ **Terraform deployment**
- ✅ **Lambda function packaging**
- ✅ **S3 frontend deployment**
- ✅ **S3 admin deployment**
- ✅ **Automatic version updates**

## 🎯 **Expected Results After Deployment**

After successful GitHub Actions run, you'll have:
- **5 DynamoDB tables** (skills, projects, certifications, adrs, versions)
- **2 S3 buckets** (frontend + admin with website hosting)
- **API Gateway** ready for Lambda functions
- **IAM roles** configured
- **Live URLs** for frontend and admin interfaces

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