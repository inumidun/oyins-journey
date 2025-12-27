# Oyin's Journey - Deployment Runbook

## 📋 **Current Status**
- **Phase**: Infrastructure Foundation
- **Status**: AWS Credentials Issue
- **Next Action**: Fix AWS CLI configuration

---

## 🚀 **Deployment Checklist**

### ✅ **Phase 1: Project Setup (COMPLETED)**
- [x] Project structure created
- [x] Terraform configuration written
- [x] Lambda functions coded
- [x] Frontend and admin interfaces created
- [x] Sample data scripts prepared

### ✅ **Phase 2: AWS Infrastructure (DESTROYED)**
**Status**: ✅ CLEANED UP

**Action**: Ran `terraform destroy` to clean up all resources
**Reason**: Switching to GitHub Actions for proper CI/CD

### 🔄 **Phase 3: GitHub Actions Setup (CURRENT)**
**Status**: 🔄 IN PROGRESS

**Next Steps**:
1. [ ] Create GitHub repository
2. [ ] Add AWS credentials as GitHub Secrets
3. [ ] Push code to GitHub
4. [ ] Monitor GitHub Actions deployment
5. [ ] Verify infrastructure creation

**Files Created**:
- ✅ `GITHUB_ACTIONS_SETUP.md` - Complete setup guide
- ✅ `.github/workflows/deploy.yml` - CI/CD pipeline ready

**Benefits of GitHub Actions Approach**:
- ✅ **Proper CI/CD** - Automated deployments on code changes
- ✅ **Version Control** - All changes tracked in Git
- ✅ **Collaboration** - Easy to share and contribute
- ✅ **Professional** - Industry standard DevOps practices
- [ ] Package Lambda functions
- [ ] Deploy to AWS Lambda
- [ ] Configure API Gateway endpoints
- [ ] Test API endpoints

### 🌐 **Phase 4: Frontend Deployment (PLANNED)**
- [ ] Upload frontend to S3
- [ ] Upload admin interface to S3
- [ ] Configure S3 website hosting
- [ ] Test website access

### 📊 **Phase 5: Data Population (PLANNED)**
- [ ] Run populate_data.py script
- [ ] Verify data in DynamoDB
- [ ] Test API responses

### 🌍 **Phase 6: Domain Setup (PLANNED)**
- [ ] Purchase domain (oyintech.dev)
- [ ] Configure Route 53
- [ ] Set up CloudFront + SSL
- [ ] Update DNS records

---

## 🛠️ **Troubleshooting Guide**

### **AWS Credentials Issues**
**Problem**: `InvalidClientTokenId` error
**Solutions**:
1. **Restart terminal** (environment variables cached)
2. **Run `aws configure`** with fresh credentials
3. **Check system time** (must be synchronized)
4. **Verify region** (use us-east-1)

### **Terraform Issues**
**Problem**: Provider download failures
**Solutions**:
1. **Check network connectivity**
2. **Try different network/VPN**
3. **Use older provider versions**
4. **Manual AWS Console setup as fallback**

---

## 📝 **Commands Reference**

### **AWS CLI Setup**
```bash
# Configure credentials
aws configure

# Test connection
aws sts get-caller-identity

# List configuration
aws configure list
```

### **Terraform Commands**
```bash
# Initialize
terraform init

# Plan deployment
terraform plan

# Apply changes
terraform apply

# Show outputs
terraform output
```

### **Deployment Commands**
```bash
# Deploy infrastructure
cd infrastructure && terraform apply

# Populate data
cd scripts && python populate_data.py

# Deploy frontend
aws s3 sync frontend/ s3://bucket-name
aws s3 sync admin/ s3://admin-bucket-name
```

---

## 🎯 **Success Criteria**

### **Phase 2 Complete When**:
- [ ] `aws sts get-caller-identity` works
- [ ] `terraform apply` succeeds
- [ ] All DynamoDB tables created
- [ ] S3 buckets created and configured
- [ ] IAM roles created

### **Project Complete When**:
- [ ] All APIs return data
- [ ] Frontend displays CV data
- [ ] Admin interface can add data
- [ ] Domain is live with SSL
- [ ] All endpoints tested

---

## 📅 **Session Log**

### **Session 1 - Initial Setup**
- ✅ Created project structure
- ✅ Wrote Terraform configuration
- ✅ Created Lambda functions
- ✅ Built frontend and admin interfaces

### **Session 2 - Infrastructure Deployment**
- ⚠️ **BLOCKED**: AWS credentials invalid
- ⚠️ **ISSUE**: Environment variables cached
- 🔧 **ACTION**: Used `setx` to clear variables
- 📋 **NEXT**: Restart terminal and reconfigure AWS CLI

---

## 🔄 **Next Session Tasks**

1. **Restart terminal completely**
2. **Run `aws configure` with valid credentials**
3. **Test `aws sts get-caller-identity`**
4. **Deploy infrastructure with `terraform apply`**
5. **Update this runbook with results**

---

*Last Updated: Current Session*
*Next Update: After AWS credentials fixed*