
# Tagging base
tags = {
  Application = "ebs-snapshot"
  Version = "1.1"
  Owner = "IT/Infra/Hosting"
  Owner_email = "bonduelle_im@bonduelle.com"
  Chargeback  = "Core"
  Customer = "IT/Infra/Hosting"
  Customer_email = "bonduelle_im@bonduelle.com"
  New_service = "no"
}

lambda_name = "ebs-snapshot"
lambda_log_retention = 30
function = "ec2_operator"
schedule_expression = "cron(0/15 * * * ? *)"
handler = "main"
