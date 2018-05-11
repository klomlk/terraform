# Terraform Configuration
terraform {
  backend "s3" {
    bucket = "bonduelle-sandbox-tfstate"
    key    = "sandbox/automation/auto-stop-start-v2"
    region = "eu-west-1"
  }
}
