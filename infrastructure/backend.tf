terraform {
  backend "s3" {
    bucket         = "oyins-journey-terraform-state"
    region         = "us-east-1"
    dynamodb_table = "oyins-journey-terraform-locks"
    encrypt        = true
     # key is set dynamically via -backend-config
  }
}