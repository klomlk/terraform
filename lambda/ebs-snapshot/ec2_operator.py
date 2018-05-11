#!/usr/bin/python

# Script: EC2 Backup Snapshots v1.1
# Created by Florian for Bonduelle Compagny
# Date: 2018-01-04

import boto3
import collections
import datetime

ec = boto3.client('ec2', region_name='eu-west-1')

def main(event, context):
    reservations = ec.describe_instances(
        Filters=[
            {'Name': 'tag:Backup', 'Values': ['Yes']},
        ]
    ).get(
        'Reservations', []
    )

    instances = sum(
        [
            [i for i in r['Instances']]
            for r in reservations
        ], [])

    to_tag = collections.defaultdict(list)
    for instance in instances:
        try:
            retention_days = [
                int(t.get('Value')) for t in instance['Tags']
                if t['Key'] == 'Retention'][0]
        except IndexError:
            retention_days = 7

        for dev in instance['BlockDeviceMappings']:
            if dev.get('Ebs', None) is None:
                continue
            vol_id = dev['Ebs']['VolumeId']
            for name in instance['Tags']:
                Instancename = name['Value']
                key = name['Key']
                if key == 'Name':
                    ins_name = Instancename
                    print("Found EBS volume {0} on instance {1}".format(vol_id, instance['InstanceId']))

            for name in instance['Tags']:
                Instancename = name['Value']
                key = name['Key']
                if key == 'Name':
                    snap = ec.create_snapshot(
                        VolumeId=vol_id,
                        Description=Instancename,
                    )
                    print("snap {0}".format(snap))

            to_tag[retention_days].append(snap['SnapshotId'])

            for retention_days in to_tag.keys():
                delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
                delete_fmt = delete_date.strftime('%Y-%m-%d')
                snap = snap['Description'] + str('_backup_')
                snapshot = snap + str(datetime.date.today())
                ec.create_tags(
                    Resources=to_tag[retention_days],
                    Tags=[
                        {'Key': 'DeleteOn', 'Value': delete_fmt},
                        {'Key': 'Name', 'Value': snapshot},
                    ]
                )
        to_tag.clear()
