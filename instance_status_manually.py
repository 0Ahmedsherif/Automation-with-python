import boto3

ec2_client = boto3.client('ec2', region_name="us-east-1")

statuses = ec2_client.describe_instance_status()
for status in statuses['InstanceStatuses']:
    state = status['InstanceState']['Name']
    ins_status = status['InstanceStatus']['Status']
    sys_status = status['SystemStatus']['Status']
    print(f"Instance: {status['InstanceId']} is: {state} with instance status {ins_status} and system status "
        f"{sys_status}")