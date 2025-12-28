# Domain Setup Guide

## Recommended Domain Strategy

### Primary Domain: `oyintech.dev` or `oyintech.cloud`

This single domain can host all your projects using subdomains:

```
oyintech.dev                    # Main portfolio/landing page
├── journey.oyintech.dev        # This CV system (frontend)
├── admin.oyintech.dev          # Admin interface
├── api.oyintech.dev           # API endpoints
├── blog.oyintech.dev          # Technical blog
├── project1.oyintech.dev      # Future project 1
├── project2.oyintech.dev      # Future project 2
└── docs.oyintech.dev          # Documentation
```

## Route 53 Setup Steps

### 1. Purchase Domain
```bash
# Check availability
aws route53domains check-domain-availability --domain-name oyintech.dev

# Purchase domain (if available)
aws route53domains register-domain --domain-name oyintech.dev --duration-in-years 1
```

### 2. Create Hosted Zone
```bash
aws route53 create-hosted-zone --name oyintech.dev --caller-reference $(date +%s)
```

### 3. Add to Terraform
Add this to your `infrastructure/main.tf`:

```hcl
# Route 53 Hosted Zone
resource "aws_route53_zone" "main" {
  name = var.domain_name
}

# CloudFront Distribution for Frontend
resource "aws_cloudfront_distribution" "frontend" {
  origin {
    domain_name = aws_s3_bucket_website_configuration.frontend.website_endpoint
    origin_id   = "S3-${aws_s3_bucket.frontend.bucket}"
    
    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  enabled             = true
  default_root_object = "index.html"

  aliases = ["journey.${var.domain_name}"]

  default_cache_behavior {
    allowed_methods        = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "S3-${aws_s3_bucket.frontend.bucket}"
    compress               = true
    viewer_protocol_policy = "redirect-to-https"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }

  viewer_certificate {
    acm_certificate_arn = aws_acm_certificate.cert.arn
    ssl_support_method  = "sni-only"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
}

# ACM Certificate
resource "aws_acm_certificate" "cert" {
  domain_name               = var.domain_name
  subject_alternative_names = ["*.${var.domain_name}"]
  validation_method         = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

# Route 53 Records
resource "aws_route53_record" "frontend" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "journey.${var.domain_name}"
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.frontend.domain_name
    zone_id                = aws_cloudfront_distribution.frontend.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "admin" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "admin.${var.domain_name}"
  type    = "CNAME"
  ttl     = 300
  records = [aws_s3_bucket_website_configuration.admin.website_endpoint]
}

# Variables
variable "domain_name" {
  description = "Domain name"
  type        = string
  default     = "oyintech.dev"
}
```

## Cost Breakdown (Annual)

| Service | Cost |
|---------|------|
| Domain (.dev) | ~$12/year |
| Route 53 Hosted Zone | $0.50/month = $6/year |
| CloudFront | Free tier: 1TB/month |
| ACM Certificate | Free |
| **Total** | **~$18/year** |

## Benefits of This Approach

1. **Single Domain Cost** - One domain for all projects
2. **Professional Subdomains** - Clean, organized structure
3. **SSL Everywhere** - Wildcard certificate covers all subdomains
4. **Scalable** - Easy to add new projects
5. **SEO Friendly** - All projects under your brand

## Alternative Domains

If `oyintech.dev` is taken:
- `oyintech.cloud`
- `oyinengineering.dev`
- `oyinbuilds.dev`
- `oyin.engineer`
- `oyincloud.dev`

## Next Steps

1. Check domain availability
2. Purchase domain in Route 53
3. Update Terraform with domain configuration
4. Deploy with SSL certificates
5. Test all subdomains