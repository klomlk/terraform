# Terraform Configuration
terraform {
  backend "s3" {
    bucket = "bonduelle-tfstate"
    key    = "prod/automation/auto-stop-start-v2"
    region = "eu-west-1"
  }
}
