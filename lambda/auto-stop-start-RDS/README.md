Introduction
============

This Lamdba is intented to start and stop RDS resources. Its actions are based on the resource's tags.

Tags to be used :

"Auto_stop"
"Auto_start"

These two tags should have cron-style values such as 0 1 . . . for 1 AM erveryday. Note that the dots '.' replace the original star '*' in cron format.
The script will substitute these dots with stars, then proceed to start or stop the instances.
This TF deploys the Lambda itself and its dependencies, with the associated IAM Role / Policy, and also the CloudWatch Rule that will trigger it every 15 minutes.