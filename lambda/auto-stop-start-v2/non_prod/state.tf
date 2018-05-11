# Terraform Configuration
terraform {
  backend "s3" {
    bucket = "bonduelle-nonprod-tfstate"
    key    = "non_prod/automation/auto-stop-start-v2"
    region = "eu-west-1"
  }
}
