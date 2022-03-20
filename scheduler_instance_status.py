import boto3
import schedule


ec2_client = boto3.client('ec2', region_name="us-east-1")

def check_instance_status():
    statuses = ec2_client.describe_instance_status(
      IncludeAllInstances=True
    )
    for status in statuses['InstanceStatuses']:
        state = status['InstanceState']['Name']
        ins_status = status['InstanceStatus']['Status']
        sys_status = status['SystemStatus']['Status']
        print(f"Instance: {status['InstanceId']} is: {state} with instance status {ins_status} and system status "
              f"{sys_status}")


schedule.every(5).minutes.do(check_instance_status)
# schedule.every().day.at("10:30").do(check_instance_status)
# schedule.every().monday.at("12:00").do(check_instance_status)
# etc...
while True:
    schedule.run_pending()      # this will execute the scheduler