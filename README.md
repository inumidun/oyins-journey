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
- **S3 + CloudFront** - Frontend hosting
- **CloudWatch** - Observability
- **GitHub Actions** - CI/CD

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
- **Backend**: AWS Lambda (Python)
- **Database**: DynamoDB
- **Frontend**: React/JavaScript
- **CI/CD**: GitHub Actions