# Oyin's Journey - Development Log

## Project Overview
**Oyin's Journey** is a living, deployed cloud architecture that serves as a queryable, versioned CV system. Instead of a static resume, this demonstrates cloud engineering skills through a real, working system.

## Development Timeline

### Phase 1: Foundation Setup ✅
**Date**: Initial Setup
**Completed**:
- [x] Project structure created
- [x] Renamed from "Living Architecture Resume" to "Oyin's Journey" for better branding
- [x] Terraform infrastructure setup
- [x] DynamoDB tables: skills, projects, adrs, versions, certifications
- [x] Lambda functions: skills, projects, adrs, version, certifications
- [x] Basic HTML frontend
- [x] GitHub Actions CI/CD pipeline
- [x] Sample data population script

**Key Decisions**:
- **Project Name**: Changed to "Oyin's Journey" for domain-friendly naming
- **Architecture**: Serverless-first (Lambda + DynamoDB + API Gateway)
- **Database**: DynamoDB with GSIs for queryable skills and certifications
- **Frontend**: Simple HTML/JS for MVP, can upgrade to React later

### Phase 2: Core Features ✅
**Completed**:
- [x] Skills API with category filtering
- [x] Projects API with individual project lookup
- [x] Architecture Decision Records (ADRs) API
- [x] Version tracking system
- [x] **NEW**: Certifications API with provider filtering
- [x] Frontend integration with all endpoints
- [x] CORS configuration for API access

**API Endpoints**:
- `GET /skills?category=devops&cloud=aws`
- `GET /projects` and `GET /projects/{id}`
- `GET /certifications?provider=aws&status=active`
- `GET /architecture/decisions`
- `GET /version`

### Phase 3: Admin Interface ✅
**Completed**:
- [x] Admin web interface for managing CV data
- [x] Forms for adding skills, certifications, projects, ADRs
- [x] Admin Lambda function for POST operations
- [x] Separate S3 bucket for admin interface
- [x] Domain strategy documentation

**Admin Features**:
- Add skills with categories and proficiency levels
- Add certifications with provider filtering
- Add projects with status tracking
- Add Architecture Decision Records
- No-code data management

### Phase 1: Infrastructure Foundation 🔄
**Date**: Current Deployment
**Status**: Switching to Manual Setup

**Step 1.1**: Deploy Core Infrastructure
- [x] Configure AWS CLI (credentials need to be valid)
- [x] Terraform blocked by network - switching to manual setup
- [ ] Create DynamoDB tables manually
- [ ] Create S3 buckets manually
- [ ] Create IAM roles manually
- [ ] Create API Gateway manually

**Issues Resolved**:
- Network connectivity blocking Terraform → Using manual AWS Console setup
- Created MANUAL_SETUP.md with step-by-step instructions

**Current Approach**: Manual AWS Console Setup
1. Create 5 DynamoDB tables with GSIs
2. Create 2 S3 buckets (frontend + admin)
3. Create IAM role for Lambda functions
4. Create API Gateway
5. Deploy Lambda functions

**Next Steps**:
- Follow MANUAL_SETUP.md guide
- Create resources in AWS Console
- Deploy Lambda functions
- Upload frontend files

### Phase 2: Domain Setup 🔄
**Planned**:
- [ ] Purchase domain (oyintech.dev recommended)
- [ ] Set up Route 53 hosted zone
- [ ] Configure CloudFront with SSL
- [ ] Deploy admin interface
- [ ] Test all endpoints in production

### Phase 5: Next Steps 🔄
**Planned**:
- [ ] Deploy to AWS and test all endpoints
- [ ] Add Lambda function deployment to Terraform
- [ ] Set up custom domain with Route 53
- [ ] Add CloudWatch dashboards for observability
- [ ] Implement API authentication (optional)
- [ ] Add more sample data
- [ ] Create documentation site

## Technical Architecture

### Infrastructure (Terraform)
```
├── DynamoDB Tables
│   ├── oyins-journey-skills (GSI: CategoryIndex)
│   ├── oyins-journey-projects
│   ├── oyins-journey-certifications (GSI: ProviderIndex)
│   ├── oyins-journey-adrs
│   └── oyins-journey-versions
├── S3 Bucket (Static Website)
├── API Gateway
└── Lambda IAM Role & Policies
```

### Lambda Functions
```
├── skills.py - Skills querying with filters
├── projects.py - Project listing and details
├── certifications.py - Certification management
├── adrs.py - Architecture decisions
└── version.py - Version tracking
```

### Data Models

#### Skills
```json
{
  "skill_id": "aws-lambda",
  "name": "AWS Lambda",
  "category": "cloud",
  "proficiency": "advanced",
  "technologies": ["Python", "Serverless"],
  "evidence_links": ["github.com/..."],
  "usage_count": 15
}
```

#### Certifications
```json
{
  "cert_id": "aws-saa-c03",
  "name": "AWS Certified Solutions Architect",
  "provider": "aws",
  "earned_date": "2024-01-15",
  "expiry_date": "2027-01-15",
  "status": "active",
  "verification_url": "aws.amazon.com/verification/..."
}
```

## Deployment Commands

### Initial Setup
```bash
# Infrastructure
cd infrastructure
terraform init
terraform apply

# Data Population
cd ../scripts
python populate_data.py

# Frontend Deployment
aws s3 sync frontend/ s3://bucket-name
```

### Domain Suggestions
- `oyinsjourney.com`
- `oyin.dev`
- `oyintech.cloud`
- `journey.oyin.dev`

## Key Benefits Demonstrated
1. **Cloud Architecture** - Serverless, scalable, cost-effective
2. **Infrastructure as Code** - Complete Terraform setup
3. **API Design** - RESTful endpoints with proper responses
4. **DevOps** - CI/CD pipeline with GitHub Actions
5. **Security** - IAM least privilege, CORS configuration
6. **Observability** - CloudWatch integration ready
7. **Cost Optimization** - Free-tier friendly architecture

## Next Review Points
- [ ] Test all API endpoints after deployment
- [ ] Verify CORS configuration
- [ ] Check Lambda function permissions
- [ ] Validate DynamoDB GSI queries
- [ ] Test CI/CD pipeline

---
*This log tracks the evolution of Oyin's Journey from concept to deployed system.*