# Terraform Configuration
terraform {
  backend "s3" {
    bucket = "bonduelle-nonprod-tfstate"
    key    = "non_prod/automation/auto-stop-start-RDS"
    dynamodb_table = "terragrunt_locks"
    region = "eu-west-1"
  }
}
