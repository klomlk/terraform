# Terraform Configuration
terraform {
  backend "s3" {
    bucket = "bonduelle-nonprod-tfstate"
    key    = "non_prod/automation/ebs-snapshot"
    region = "eu-west-1"
  }
}
