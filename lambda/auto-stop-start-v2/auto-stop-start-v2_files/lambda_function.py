#!/usr/bin/python

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
import pytz


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
    except:
        action = False
        print("time_to_action {}".format(action))
    return action

# Main function of this program ; SetTimezone ; CheckTags ; CompTimezone&Tags
def main(event, toto2):
    now = datetime.datetime.now(pytz.timezone('Europe/Paris'))

    # Get period from event. Period (in minutes) sent as an input in Cloudwatch
    period = int(event["Period"])
    #period = 15

    # Go through all regions # Plus besoin, on limite la recherche sur eu-west-1
    try:
        print("Before connect to region")
        ec2 = boto3.resource("ec2", "eu-west-1")  # nouvelle syntaxe boto3
        all_instances = ec2.instances.all()
        name =''

        for instance in all_instances:
            start_list = list()
            stop_list = list()
            for tag in instance.tags:
                if tag["Key"] == "Name":
                    name = tag["Value"]
                else:
                    name = "Unknown"
            state = instance.state["Name"]
            
            # Check AutoStart and AutoStop tags
                
            start_sched = [tag["Value"] for tag in instance.tags if tag['Key'] == "Auto_start"]
            
            stop_sched = [tag["Value"] for tag in instance.tags if tag['Key'] == "Auto_stop"]
           
            
            if "None" in stop_sched or "none" in stop_sched or stop_sched == [] and "None" in start_sched or start_sched == [] or "none" in start_sched:
                print("############# Skipping one instance #############")
                print("No stop nor start tags found, skipping this instance (" + instance.id + ')')
                continue
                        
            print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{5}\t{6}\t{7}\t".format(
                "eu-west-1", name, instance.id, instance.instance_type, instance.launch_time, state, start_sched[0],
                stop_sched[0]))
            
            if state == "running":
                if time_to_action(stop_sched, now, period * -60):
                    stop_list.append(instance.id)
                    print("******* affichage de stop_list ********\n",stop_list)
                    if len(stop_list) > 0:
                        retu = boto3.client("ec2").stop_instances(InstanceIds = stop_list, DryRun=False)
                        
                        print("stopped instances {0}\n".format(instance.id),"############## next instance ##############" )
            if state == "stopped":
                if time_to_action(start_sched, now, period * 60):
                    start_list.append(instance.id)
                    print("******* affichage de start_list ********\n",start_list)
                    if len(start_list) > 0:
                        retu = boto3.client("ec2").start_instances(InstanceIds = start_list, DryRun=False)
                        print("started instance {0}\n".format(instance.id),"############## next instance ##############")

    except Exception as e:
        print('Exception error in eu-west-1: {0}'.format(e))
## End of this program
