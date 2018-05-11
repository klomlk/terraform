#!/usr/bin/python

#
# A faire !
## Trouver comment lister les instances RDS : OK
## Récupérer les noms : OK
## Recuperer leurs états
## Recuperer les tags : OK
##
#
# Script: EC2 Start and Stop v1.1
# Created by Maxime, modified by Gekko
# Date: 2017-12-13

# Permissions for this script: ec2:Stop*, ec2:Start*, ec2:RunInstances,
# ec2:DescribeTags and ec2:DescribeInstances.

# Permissions for CloudWatch: logs:PutLogEvents,
# logs:CreateLogStream and logs:CreateLogGroup

import croniter
import datetime
import boto3
import re
import pytz
#global action
# Return "True" if the CRON schedule falls between now and now+seconds
def time_to_action(sched, now, seconds):
# sched est une liste, contenant une seconde liste
    action = False
    try:
        cron = croniter.croniter(sched[0], now)
        d1 = now + datetime.timedelta(0, seconds)
        if seconds > 0:
            #### Demarrage #####
            d2 = cron.get_next(datetime.datetime)
            if now <= d1 and d2 <= d1 and now <= d2:
                action = True
        else:
            #### Arret ####
            d2 = cron.get_prev(datetime.datetime)
            if d1 <= now and d1 <= d2 and d2 <= now:
                action = True
            		
        print("now {}".format(now))
        print("d1 {}".format(d1))
        print("d2 {}".format(d2))
        print("time_to_action {}".format(action))
    except Exception as e:
        action = False
        print(e)
        print("time_to_action {}".format(action))
    return action

# Main function of this program ; SetTimezone ; CheckTags ; CompTimezone&Tags
def main(event, toto2):

    now = datetime.datetime.now(pytz.timezone('Europe/Paris'))

    # Get period from event. Period (in minutes) sent as an input in Cloudwatch
    period = int(event["Period"])
    #period = 15

    
    ####### Definition de l'expression reguliere a chercher:
    pattern = re.compile('\.')
    #######

    try:
        print("Before connect to region")
        rds = boto3.client("rds")
            # liste de nom de toutes les instances db
        for instance in rds.describe_db_instances()["DBInstances"]:
            name = instance["DBInstanceIdentifier"]
            arn = instance['DBInstanceArn']
            tags = rds.list_tags_for_resource(ResourceName=arn)["TagList"]
            state = instance["DBInstanceStatus"]
            start =list()
            stop = list()
            stop_sched = list()
            start_sched = list()

            # Check AutoStart and AutoStop tags
            for tag in tags:

                if "Auto_start" == tag["Key"]:
                    new_value = re.sub(pattern,"*",tag["Value"])  #### Insérer ici la substitution regex
                    start_sched.append(new_value)

                if "Auto_stop" == tag["Key"]:
                    new_value = re.sub(pattern, "*", tag["Value"])  #### Insérer ici la substitution regex
                    stop_sched.append(new_value)
            
            if "None" in stop_sched or "none" in stop_sched or stop_sched == [] and "None" in start_sched or start_sched == [] or "none" in start_sched:
                print("############# Skipping one instance #############")
                print("No stop nor start tags found, skipping this instance")
                continue

            print("eu-west-1",'\t',name,"\t",instance["DBInstanceClass"],'\t',
                  instance["InstanceCreateTime"],"\t",state,"\t",start_sched,"\t",stop_sched)
            #print(start_sched[0])
            # Queue up instances that have the start time falls between now and the next 30 minutes
            if state == "stopped" and time_to_action(start_sched, now, period * 60):
                start = rds.start_db_instance(DBInstanceIdentifier=name)
                print("start_instances {0} - {1}".format(start["DBInstance"]["DBInstanceIdentifier"],
                                                  start["DBInstance"]["DBInstanceClass"]))

            # Queue up instances that have the stop time falls between 30 minutes ago and now
            if state == "available" and time_to_action(stop_sched, now, period * -60):
                stop = rds.stop_db_instance(DBInstanceIdentifier=name)
                print("stop_instances {0} - {1}".format(stop["DBInstance"]["DBInstanceIdentifier"],
                                                 stop["DBInstance"]["DBInstanceClass"]))

    except Exception as e:
        print('Exception error in eu-west-1: {0}'.format(e))
# End of this program