# Branching Strategy - Oyin's Journey

## 🌿 **Branch Structure**

### **`dev`** - Development Branch
- **Purpose**: Active development and feature work
- **Deployment**: Dev environment (`dev-oyintech.dev`)
- **Auto-deploy**: ✅ On every push
- **Terraform workspace**: `dev`

### **`test`** - Testing Branch  
- **Purpose**: Integration testing and QA
- **Deployment**: Test environment (`test-oyintech.dev`)
- **Auto-deploy**: ✅ On every push
- **Terraform workspace**: `test`

### **`main`** - Production Branch
- **Purpose**: Production-ready code
- **Deployment**: Production environment (`oyintech.dev`)
- **Auto-deploy**: ✅ On every push (after manual approval)
- **Terraform workspace**: `default`

## 🔄 **Workflow**

```
dev → test → main
 ↓     ↓      ↓
dev   test   prod
env   env    env
```

## 🚀 **Getting Started**

### **1. Create and Switch to Dev Branch**
```bash
# Create dev branch
git checkout -b dev

# Push dev branch to remote
git push -u origin dev

# Set dev as default working branch
git checkout dev
```

### **2. Create Test Branch**
```bash
# Create test branch from main
git checkout main
git checkout -b test
git push -u origin test
```

### **3. Development Workflow**
```bash
# Work on dev branch
git checkout dev

# Make changes
git add .
git commit -m "feat: add new feature"
git push origin dev

# When ready for testing
git checkout test
git merge dev
git push origin test

# When ready for production
git checkout main
git merge test
git push origin main
```

## 🏗️ **Environment Differences**

| Environment | Branch | Domain | DynamoDB Tables | S3 Buckets |
|-------------|--------|--------|----------------|------------|
| **Dev** | `dev` | `dev-oyintech.dev` | `dev-*` | `dev-*` |
| **Test** | `test` | `test-oyintech.dev` | `test-*` | `test-*` |
| **Prod** | `main` | `oyintech.dev` | `prod-*` | `prod-*` |

## 📋 **Branch Protection Rules**

### **Main Branch**
- ✅ Require pull request reviews
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ✅ Restrict pushes to admins only

### **Test Branch**
- ✅ Require status checks to pass
- ✅ Allow direct pushes from dev

### **Dev Branch**
- ✅ No restrictions (development freedom)

## 🎯 **Current Status**

**Starting on `dev` branch for all initial development work.**