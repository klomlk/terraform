# Terraform Configuration
terraform {
  backend "s3" {
    bucket = "bonduelle-sandbox-tfstate"
    key    = "prod/automation/auto-stop-start-RDS"
    region = "eu-west-1"
  }
}
