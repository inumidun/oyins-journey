# Oyin's Journey

A **real, deployed cloud system that _is_ your CV** — not a PDF, not a portfolio site — but a **self-documenting, queryable, versioned cloud architecture** that proves your skills by existing.

## 🚀 Quick Start

```bash
# Deploy infrastructure
cd infrastructure
terraform init
terraform plan
terraform apply

# Deploy API
cd ../api
# Deploy Lambda functions

# Deploy frontend
cd ../frontend
# Deploy to S3/CloudFront
```

## 🏗️ Architecture

- **API Gateway + Lambda** - Serverless API endpoints
- **DynamoDB** - Skills, projects, certifications, ADRs storage
- **S3 + CloudFront** - Private buckets with CDN (OAC)
- **CloudWatch** - Observability
- **GitHub Actions** - Multi-environment CI/CD

## 📡 API Endpoints

- `GET /skills` - Query skills and technologies
- `GET /projects` - List projects and experience
- `GET /certifications` - List certifications and credentials
- `GET /architecture/decisions` - Architecture Decision Records
- `GET /version` - Current CV version

## 🌐 **Admin Interface**

Manage your CV data without touching code:
- **Skills Management** - Add/edit skills with categories
- **Certifications** - Track certifications with expiry dates
- **Projects** - Manage project portfolio
- **ADRs** - Document architecture decisions

Access: `admin.oyintech.dev` (after domain setup)

## 🌍 **Domain Strategy**

Recommended: **`oyintech.dev`** (~$18/year total)
- `journey.oyintech.dev` - CV system
- `admin.oyintech.dev` - Admin interface
- `api.oyintech.dev` - API endpoints
- `project1.oyintech.dev` - Future projects

## 🛠️ Tech Stack

- **Infrastructure**: Terraform
- **Backend**: AWS Lambda (Python 3.13)
- **Database**: DynamoDB
- **Frontend**: React/JavaScript
- **CDN**: CloudFront with Origin Access Control
- **CI/CD**: GitHub Actions (Multi-environment)

## 📚 Documentation

Comprehensive documentation is available in the [`docs/`](./docs/) folder:

### Setup & Deployment
- [AWS Setup Guide](./docs/AWS_SETUP.md) - AWS account configuration
- [Backend Setup Guide](./docs/BACKEND_SETUP.md) - **Remote state backend setup**
- [GitHub Actions Setup](./docs/GITHUB_ACTIONS_SETUP.md) - CI/CD pipeline setup
- [Deployment Runbook](./docs/DEPLOYMENT_RUNBOOK.md) - Step-by-step deployment
- [Manual Setup](./docs/MANUAL_SETUP.md) - Manual deployment instructions

### Development
- [Branching Strategy](./docs/BRANCHING_STRATEGY.md) - Git workflow and environments
- [Development Log](./docs/DEVELOPMENT_LOG.md) - Development progress tracking
- [Architecture Decisions](./docs/ARCHITECTURE_DECISIONS.md) - **Complete ADR with all design decisions**

### Infrastructure
- [Domain Setup](./docs/DOMAIN_SETUP.md) - Custom domain configuration

## 🏛️ **Architecture Decisions**

All architectural and design decisions are documented in our comprehensive [Architecture Decision Record (ADR)](./docs/ARCHITECTURE_DECISIONS.md), including:

- Multi-environment strategy (dev/test/prod)
- Private S3 + CloudFront with OAC
- Modular GitHub Actions workflows
- Terraform workspace strategy
- Security-first CI/CD pipeline
- Technology stack rationale

## 🌿 **Development Workflow**

```bash
# Work on dev branch
git checkout dev
git add .
git commit -m "your changes"
git push origin dev  # Auto-deploys to dev environment

# When ready for testing
git checkout test
git merge dev
git push origin test  # Auto-deploys to test environment

# When ready for production
git checkout main
git merge test
git push origin main  # Auto-deploys to production
```

## 🔒 **Security & Compliance**

- ✅ **Remote State Management** - S3 backend with DynamoDB locking
- ✅ Private S3 buckets with CloudFront OAC
- ✅ IAM roles with least privilege
- ✅ Security scanning in CI/CD pipeline
- ✅ Environment isolation with separate state files
- ✅ AWS Well-Architected Framework compliance

---

**This is not just a portfolio — it's a living, breathing cloud architecture that demonstrates real-world engineering skills.**