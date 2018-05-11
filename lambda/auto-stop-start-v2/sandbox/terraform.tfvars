
# Tagging base
tags = {
  Application = "auto-stop-start-v2"
  Version = "1.1"
  Owner = "IT/Infra/Hosting"
  Owner_email = "bonduelle_im@bonduelle.com"
  Chargeback = "Core"
  Customer = "IT"
  Custumer_email = "bonduelle_im@bonduelle.com"
  New_service = "no"
}

lambda_name = "auto-stop-start-v2"
lambda_log_retention = 30
function = "lambda_function"
schedule_expression = "cron(0/10 * * * ? *)"
handler = "main"
timeout_period = 3
