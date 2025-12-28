# Architecture Decision Record (ADR) - Oyin's Journey

## Overview
This document captures all architectural and design decisions made for "Oyin's Journey" - a living architecture resume system that demonstrates cloud engineering skills through actual deployed infrastructure.

---

## ADR-001: Multi-Environment Strategy

**Date**: 2024-12-19  
**Status**: Accepted  
**Decision Makers**: Development Team

### Context
Need to support development, testing, and production environments with proper isolation and deployment strategies.

### Decision
Implement three-tier environment strategy:
- `dev` branch → Development environment (`oyins-journey-dev-*`)
- `test` branch → Testing environment (`oyins-journey-test-*`) 
- `main` branch → Production environment (`oyins-journey-prod-*`)

### Rationale
- **Risk Mitigation**: Changes tested in dev before test, then production
- **Resource Isolation**: Each environment has separate AWS resources
- **Cost Control**: Dev/test environments can be smaller/cheaper
- **AWS Best Practice**: Follows Well-Architected Framework

### Consequences
- **Positive**: Safe deployment pipeline, environment parity
- **Negative**: Increased infrastructure complexity and costs
- **Mitigation**: Use Terraform workspaces for resource management

---

## ADR-002: Private S3 + CloudFront Architecture

**Date**: 2024-12-19  
**Status**: Accepted  
**Decision Makers**: Development Team

### Context
Initial design used public S3 buckets for static website hosting, but this violates security best practices.

### Decision
Replace public S3 buckets with private S3 + CloudFront using Origin Access Control (OAC).

### Rationale
- **Security**: S3 buckets remain private, no public access
- **Performance**: CloudFront provides global CDN capabilities
- **Cost Optimization**: CloudFront caching reduces S3 requests
- **AWS Best Practice**: Recommended pattern for static websites
- **Compliance**: Meets enterprise security requirements

### Implementation
```hcl
# Private S3 bucket
resource "aws_s3_bucket" "frontend" {
  bucket = "${local.name_prefix}-frontend-${random_string.bucket_suffix.result}"
}

# CloudFront with OAC
resource "aws_cloudfront_origin_access_control" "frontend" {
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}
```

### Consequences
- **Positive**: Enhanced security, better performance, cost optimization
- **Negative**: Slightly more complex setup
- **Trade-off**: Accepted complexity for security benefits

---

## ADR-003: Modular GitHub Actions Workflows

**Date**: 2024-12-19  
**Status**: Accepted  
**Decision Makers**: Development Team

### Context
Initial monolithic workflow was difficult to maintain and didn't follow separation of concerns.

### Decision
Split into focused, reusable workflow components:
- `main.yml` - Orchestrator with conditional logic
- `infrastructure.yml` - Terraform deployments
- `unit-tests.yml` - Code quality and testing
- `web-app.yml` - Application deployments

### Rationale
- **Maintainability**: Easier to update individual components
- **Reusability**: Workflows can be called from multiple places
- **Parallel Execution**: Independent jobs run concurrently
- **Conditional Deployment**: Only deploy what changed
- **AWS Best Practice**: Infrastructure as Code with proper CI/CD

### Implementation
```yaml
# Conditional deployment based on file changes
if: |
  contains(needs.setup.outputs.changed_files, 'infrastructure/') ||
  contains(needs.setup.outputs.changed_files, '.github/workflows/')
```

### Consequences
- **Positive**: Better maintainability, faster deployments, cost savings
- **Negative**: More files to manage
- **Mitigation**: Clear documentation and naming conventions

---

## ADR-004: Terraform Workspace Strategy

**Date**: 2024-12-19  
**Status**: Accepted  
**Decision Makers**: Development Team

### Context
Need to manage multiple environments with Terraform while maintaining state isolation.

### Decision
Use Terraform workspaces for environment isolation:
- `default` workspace for production (`main` branch)
- `dev` workspace for development (`dev` branch)
- `test` workspace for testing (`test` branch)

### Rationale
- **State Isolation**: Each environment has separate state files
- **Resource Naming**: Environment-specific resource names prevent conflicts
- **Cost Management**: Easy to track resources per environment
- **AWS Best Practice**: Proper environment separation

### Implementation
```hcl
# Environment-specific naming
locals {
  name_prefix = "${var.project_name}-${var.environment}"
}

# No default environment value - explicit targeting required
variable "environment" {
  description = "Environment (dev, test, prod)"
  type        = string
  # No default - must be explicitly provided
}
```

### Consequences
- **Positive**: Clean environment separation, no resource conflicts
- **Negative**: Must manage multiple state files
- **Trade-off**: Accepted complexity for proper isolation

---

## ADR-005: Security-First CI/CD Pipeline

**Date**: 2024-12-19  
**Status**: Accepted  
**Decision Makers**: Development Team

### Context
Need to implement security scanning and validation throughout the deployment pipeline.

### Decision
Implement comprehensive security scanning:
- Security scans before any deployment
- Terraform validation and security scanning
- Python code security analysis (Bandit)
- Dependency vulnerability scanning

### Rationale
- **AWS Security Best Practice**: Shift-left security approach
- **Compliance**: Meet enterprise security requirements
- **Risk Mitigation**: Catch vulnerabilities early
- **Cost Avoidance**: Prevent security incidents

### Implementation
```yaml
- name: Security scan
  run: |
    echo "🔒 Running security scans for ${{ inputs.environment }} environment"
    bandit -r api/ -f json -o bandit-report.json
    terraform validate
```

### Consequences
- **Positive**: Enhanced security posture, early vulnerability detection
- **Negative**: Slightly longer build times
- **Trade-off**: Accepted time cost for security benefits

---

## ADR-006: Python 3.13 for Lambda Functions

**Date**: 2024-12-19  
**Status**: Accepted  
**Decision Makers**: Development Team

### Context
Need to choose Python version for AWS Lambda functions and development environment.

### Decision
Use Python 3.13 (latest available version).

### Rationale
- **Performance**: Latest Python version with performance improvements
- **Security**: Latest security patches and updates
- **Features**: Access to newest language features
- **Future-Proofing**: Longer support lifecycle

### Consequences
- **Positive**: Best performance and security
- **Negative**: Potential compatibility issues with older libraries
- **Mitigation**: Thorough testing in dev environment

---

## ADR-007: Conditional Deployment Strategy

**Date**: 2024-12-19  
**Status**: Accepted  
**Decision Makers**: Development Team

### Context
Need to optimize deployment pipeline to only deploy components that have changed.

### Decision
Implement smart conditional deployment based on file changes:
- Infrastructure: Deploy only if `infrastructure/` or workflow files change
- Web App: Deploy only if `frontend/`, `admin/`, or `api/` files change
- Unit Tests: Run only if `api/` or `scripts/` files change

### Rationale
- **Cost Optimization**: Avoid unnecessary deployments
- **Speed**: Faster pipeline execution
- **Risk Reduction**: Less chance of breaking working components
- **AWS Best Practice**: Efficient resource utilization

### Implementation
```yaml
if: |
  github.event_name == 'push' && 
  (contains(needs.setup.outputs.changed_files, 'infrastructure/') || 
   contains(needs.setup.outputs.changed_files, '.github/workflows/'))
```

### Consequences
- **Positive**: Faster deployments, cost savings, reduced risk
- **Negative**: More complex workflow logic
- **Trade-off**: Accepted complexity for efficiency gains

---

## ADR-008: No Default Environment Values

**Date**: 2024-12-19  
**Status**: Accepted  
**Decision Makers**: Development Team

### Context
Initial Terraform configuration had default environment values, which could lead to accidental deployments.

### Decision
Remove all default environment values - require explicit environment targeting.

### Rationale
- **Safety**: Prevent accidental deployments to wrong environment
- **Clarity**: Explicit is better than implicit
- **AWS Best Practice**: Intentional infrastructure changes only
- **Compliance**: Audit trail requires explicit targeting

### Consequences
- **Positive**: No accidental deployments, clear intent
- **Negative**: Must always specify environment
- **Trade-off**: Accepted verbosity for safety

---

## Technology Stack Decisions

### Infrastructure
- **Terraform**: Infrastructure as Code
- **AWS**: Cloud provider
- **GitHub Actions**: CI/CD platform

### Backend Services
- **AWS Lambda**: Serverless compute (Python 3.13)
- **DynamoDB**: NoSQL database (pay-per-request)
- **API Gateway**: REST API management

### Frontend & CDN
- **S3**: Static file storage (private)
- **CloudFront**: Global CDN with OAC
- **HTML/CSS/JavaScript**: Frontend technologies

### Security & Monitoring
- **CloudWatch**: Logging and monitoring
- **IAM**: Access control
- **Bandit**: Python security scanning
- **GitHub Secrets**: Credential management

---

## Future Considerations

### Planned Enhancements
1. **Custom Domain**: Implement Route 53 with SSL certificates
2. **Monitoring**: Enhanced CloudWatch dashboards and alerts
3. **Testing**: Comprehensive unit and integration tests
4. **Security**: Advanced security scanning tools integration
5. **Performance**: Lambda performance optimization

### Potential Migrations
1. **Container Support**: Consider ECS/Fargate for larger applications
2. **Database**: Evaluate RDS for relational data needs
3. **Caching**: Consider ElastiCache for performance optimization

---

## Compliance & Best Practices

### AWS Well-Architected Framework Alignment
- ✅ **Security**: Private resources, IAM roles, security scanning
- ✅ **Reliability**: Multi-environment testing, infrastructure as code
- ✅ **Performance Efficiency**: CloudFront CDN, serverless architecture
- ✅ **Cost Optimization**: Pay-per-request pricing, conditional deployments
- ✅ **Operational Excellence**: Automated deployments, monitoring, documentation

### Security Compliance
- Private S3 buckets with CloudFront OAC
- IAM roles with least privilege access
- Security scanning in CI/CD pipeline
- No hardcoded credentials
- Environment-specific resource isolation

---

*This document is maintained as a living record of architectural decisions and will be updated as the system evolves.*