# Terraform Configuration
terraform {
  backend "s3" {
    bucket = "bonduelle-tfstate"
    key    = "prod/automation/ebs-snapshot"
    region = "eu-west-1"
  }
}
