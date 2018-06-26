
# Tagging base
tags = {
  Application = "ebs-snapshot"
}

lambda_name = "ebs-snapshot"
lambda_log_retention = 30
function = "ec2_operator"
schedule_expression = "cron(0/15 * * * ? *)"
handler = "main"
