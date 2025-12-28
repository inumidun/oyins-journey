# GitHub Actions Troubleshooting Guide

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

### **Step 1: Check Workflow Syntax**
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('.github/workflows/main.yml'))"
```

### **Step 2: Verify Action Versions**
- Check [GitHub Actions Marketplace](https://github.com/marketplace/actions/) for latest versions
- Update to latest stable releases

### **Step 3: Check Repository Settings**
- **Settings** → **Actions** → **General**
- Ensure "Allow all actions and reusable workflows" is selected

### **Step 4: Enable Debug Logging**
Add to workflow environment:
```yaml
env:
  ACTIONS_RUNNER_DEBUG: true
  ACTIONS_STEP_DEBUG: true
```

### **Step 5: Check GitHub Status**
- Visit [githubstatus.com](https://githubstatus.com) for service outages

## 📋 **Checklist for New Workflows**

- [ ] All required inputs defined in `workflow_call`
- [ ] Latest action versions used
- [ ] Proper step ordering (init before validate)
- [ ] No duplicate resource declarations
- [ ] Consistent branch targeting
- [ ] Required secrets available
- [ ] Repository permissions configured

## 🎯 **Quick Fixes Applied**

1. ✅ Updated all action versions to latest
2. ✅ Added missing workflow inputs
3. ✅ Removed environment protection
4. ✅ Fixed Terraform step ordering
5. ✅ Removed duplicate files
6. ✅ Standardized branch targeting

**Result**: Workflows now start and execute successfully! 🚀