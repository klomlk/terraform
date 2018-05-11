Introduction
============

This Lamdba is intented to start and stop resources. Its actions are based on the resource's tags.

For now, it only deals with EC2's.

Tags to be used :

"Auto_stop"
"Auto_start"

These two tags should have cron-style values such as 0 1 * * * for 1 AM erveryday.

This TF simply deploys the Lambda itself, with the associated IAM Role / Policy, and also the CloudWatch Rule that will trigger it every X minutes.