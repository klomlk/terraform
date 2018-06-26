#!/usr/bin/python
# Script: EC2 Create Snapshots v1.2
# Created by Florian for Bonduelle Compagny
# Date: 2018-01-10

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
            retention_days = 15

        for dev in instance['BlockDeviceMappings']:
            if dev.get('Ebs', None) is None:
                continue
            vol_id = dev['Ebs']['VolumeId']
            deviceName = dev['DeviceName'].split('/')[-1]
            print(deviceName)
            for name in instance['Tags']:
                Instancename = name['Value']
                key = name['Key']
                if key == 'Name':
                    ins_name = Instancename

            for name in instance['Tags']:
                Instancename = name['Value']
                key = name['Key']
                if key == 'Name':
                    snap = ec.create_snapshot(
                        VolumeId=vol_id,
                        Description = Instancename,
                    )

            to_tag[retention_days].append(snap['SnapshotId'])

            for retention_days in to_tag.keys():
                delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
                delete_fmt = delete_date.strftime('%Y-%m-%d')
                snap = snap['Description']
                snapshot = str(datetime.date.today()) + str('_') + deviceName +\
                str('_backup_') + snap
                ec.create_tags(
                    Resources=to_tag[retention_days],
                    Tags=[
                        {'Key': 'DeleteOn', 'Value': delete_fmt},
                        {'Key': 'Name', 'Value': snapshot},
                    ]
                )
            
            to_tag.clear()
