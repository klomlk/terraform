
variable "lambda_name" {
  description = "That name will be used in various resources"
}

variable "lambda_log_retention" {
  description = "Retention in days of logs sent to Cloudwatch"
}

#variable "schedule_expression" {
#  description = "cron like expression to tell when the lamdba should be trigerred"
#}

variable "function" {
  description = "Python function to be run (filename that contains the handler)"
}

variable "handler" {
  description = "Handler in function"
}

