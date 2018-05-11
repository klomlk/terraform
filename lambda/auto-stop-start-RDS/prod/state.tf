# Terraform Configuration
terraform {
  backend "s3" {
    bucket = "bonduelle-tfstate"
    key    = "prod/automation/auto-stop-start"
    region = "eu-west-1"
  }
}
