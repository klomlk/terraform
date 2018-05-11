provider "aws" {
  region = "${var.region}"
}

terraform {
  backend "s3" {}
}

###
# Policy Document
###

data "aws_iam_policy_document" "policydoc" {
  statement {
    sid = "1"
    effect = "Allow"
    actions = [
                  "logs:CreateLogGroup",
                  "logs:CreateLogStream",
                  "logs:PutLogEvents",
    ]
    resources = [
                  "arn:aws:logs:*:*:*",
    ]
    effect =  "Allow"
    actions = [
                  "ec2:Start*",
                  "ec2:Stop*",
                  "ec2:RunInstances",
                  "ec2:DescribeInstances",
                  "ec2:DescribeTags",
    ]
    resources = [
                  "*",
    ]
  }
}




###
# Zip the function and its dependences
###

data "archive_file" "functionpack" {
  type          = "zip"
  source_dir    = "${var.lambda_name}_files/"
  output_path   = "${var.lambda_name}.zip"
}


###
# The lambda itself
###

module "scheduled_lambda" {
  source                = "../../../modules/tf_aws_lambda_scheduled"
  lambda_name           = "${var.lambda_name}"
  runtime               = "python3.6"
  lambda_zipfile        = "${var.lambda_name}.zip"
  source_code_hash      = "${data.archive_file.functionpack.output_base64sha256}"
  handler               = "${var.function}.${var.handler}"
  schedule_expression   = "${var.schedule_expression}"
  iam_policy_document   = "${data.aws_iam_policy_document.policydoc.json}"
  lambda_log_retention  = "${var.lambda_log_retention}"
  tags                  = "${var.tags}"
  period                = 15
  timeout               = "${var.timeout_period}"
}
