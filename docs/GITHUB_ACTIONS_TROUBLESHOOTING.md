# GitHub Actions Troubleshooting Guide

## 🚀 **Remote State Backend Issues (NEW)**

### **1. Backend Initialization Failures**

**Problem**: S3 backend bucket doesn't exist
```
Error: Failed to get existing workspaces: S3 bucket does not exist
```

**Solution**: Ensure bootstrap script runs first
```yaml
- name: Bootstrap backend (if needed)
  run: |
    aws s3api head-bucket --bucket oyins-journey-terraform-state >/dev/null 2>&1 || {
      echo "🚀 Creating Terraform backend..."
      chmod +x bootstrap.sh
      ./bootstrap.sh
    }
```

### **2. State Lock Conflicts**

**Problem**: DynamoDB lock table issues
```
Error: Error acquiring the state lock
```

**Solutions**:
1. **Wait**: Locks usually release automatically
2. **Force unlock**: `terraform force-unlock LOCK_ID`
3. **Check table**: Verify DynamoDB table exists

### **3. Backend Configuration Conflicts**

**Problem**: Hardcoded backend key conflicts with dynamic key
```hcl
# ❌ Wrong - hardcoded key
terraform {
  backend "s3" {
    key = "infrastructure/terraform.tfstate"
  }
}

# ✅ Correct - dynamic key
terraform {
  backend "s3" {
    # key set via -backend-config
  }
}
```

**Solution**: Remove hardcoded key, use `-backend-config`

### **4. State Migration Issues**

**Problem**: Existing resources not in remote state
```
Error: resource already exists
```

**Solution**: Run migration script before deployment
```bash
./infrastructure/migrate.sh dev
```

## 🚨 **Common Startup Failures & Solutions**

### **1. Workflow Configuration Issues**

**Problem**: Missing required inputs in workflow_call
```yaml
# ❌ Wrong - missing inputs
on:
  workflow_call:

# ✅ Correct - with required inputs  
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      aws_region:
        required: true
        type: string
```

**Solution**: Always define inputs that parent workflows pass

### **2. Action Version Compatibility**

**Problem**: Using outdated action versions
```yaml
# ❌ Wrong - outdated versions
uses: actions/checkout@v3
uses: actions/setup-python@v4
uses: actions/cache@v3

# ✅ Correct - latest versions
uses: actions/checkout@v4
uses: actions/setup-python@v5
uses: actions/cache@v4
```

**Solution**: Keep actions updated to latest stable versions

### **3. GitHub Environment Protection**

**Problem**: Referencing non-existent environments
```yaml
# ❌ Wrong - environment not configured
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}

# ✅ Correct - remove if not needed
jobs:
  deploy:
    runs-on: ubuntu-latest
```

**Solution**: Remove environment protection or configure in repository settings

### **4. Terraform Module Installation**

**Problem**: Validate before init
```yaml
# ❌ Wrong - validate before init
- name: Terraform Validate
  run: terraform validate
- name: Terraform Init  
  run: terraform init

# ✅ Correct - init before validate
- name: Terraform Init
  run: terraform init
- name: Terraform Validate
  run: terraform validate
```

**Solution**: Always run `terraform init` before any other terraform commands

### **5. Duplicate File Conflicts**

**Problem**: Multiple Terraform files with same resources
```
infrastructure/
├── main.tf      # ✅ Keep
├── main-old.tf  # ❌ Remove - causes duplicates
```

**Solution**: Remove backup/old files that cause duplicate declarations

### **6. Branch Targeting Issues**

**Problem**: Inconsistent PR branch targeting
```yaml
# ❌ Wrong - allows PRs to dev
pull_request:
  branches: [dev, test, main]

# ✅ Correct - PRs only to test/main
pull_request:
  branches: [test, main]
```

**Solution**: Standardize branch protection across workflows

## 🔧 **Debugging Steps**

### **Step 1: Check Backend Status**
```bash
# Verify backend resources exist
aws s3api head-bucket --bucket oyins-journey-terraform-state
aws dynamodb describe-table --table-name oyins-journey-terraform-locks
```

### **Step 2: Test State Access**
```bash
# Test backend connectivity
terraform init -backend-config="key=test/terraform.tfstate"
terraform workspace list
```

### **Step 3: Check Workflow Syntax**
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('.github/workflows/main.yml'))"
```

### **Step 4: Verify Action Versions**
- Check [GitHub Actions Marketplace](https://github.com/marketplace/actions/) for latest versions
- Update to latest stable releases

### **Step 5: Check Repository Settings**
- **Settings** → **Actions** → **General**
- Ensure "Allow all actions and reusable workflows" is selected

### **Step 6: Enable Debug Logging**
Add to workflow environment:
```yaml
env:
  ACTIONS_RUNNER_DEBUG: true
  ACTIONS_STEP_DEBUG: true
```

## 📋 **Checklist for New Workflows**

### **Backend Requirements**
- [ ] S3 backend bucket exists
- [ ] DynamoDB locks table exists
- [ ] Backend configuration has no hardcoded key
- [ ] Bootstrap step included in workflow

### **Workflow Configuration**
- [ ] All required inputs defined in `workflow_call`
- [ ] Latest action versions used
- [ ] Proper step ordering (init before validate)
- [ ] No duplicate resource declarations
- [ ] Consistent branch targeting
- [ ] Required secrets available
- [ ] Repository permissions configured

## 🎯 **Quick Fixes Applied**

### **Remote State Backend (Latest)**
1. ✅ Implemented S3 remote backend
2. ✅ Created bootstrap and migration scripts
3. ✅ Removed hardcoded backend keys
4. ✅ Added automatic backend creation
5. ✅ Eliminated import step workarounds

### **Previous Fixes**
1. ✅ Updated all action versions to latest
2. ✅ Added missing workflow inputs
3. ✅ Removed environment protection
4. ✅ Fixed Terraform step ordering
5. ✅ Removed duplicate files
6. ✅ Standardized branch targeting

**Result**: Workflows now use proper remote state management! 🚀