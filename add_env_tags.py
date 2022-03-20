import boto3


ec2_client_virginia = boto3.client('ec2', region_name="us-east-1")  # client
ec2_resource_virginia = boto3.resource('ec2', region_name="us-east-1")  # resource

ec2_client_paris = boto3.client('ec2', region_name="eu-west-3")  # client
ec2_resource_paris = boto3.resource('ec2', region_name="eu-west-3")  # resource

instance_ids_virginia = []  # saving the ids in a list
instance_ids_paris = []

Reservations_virginia = ec2_client_virginia.describe_instances()["Reservations"]
for reservation in Reservations_virginia:
    instances = reservation["Instances"]
    for instance in instances:
        instance_ids_virginia.append(instance['InstanceId'])
print("Done!")

response_virginia = ec2_resource_virginia.create_tags(
    Resources=instance_ids_virginia,
    Tags=[
        {
            'Key': 'Env',
            'Value': 'prod'
        },
    ]
)

Reservations_paris = ec2_client_paris.describe_instances()["Reservations"]
for reservation in Reservations_paris:
    instances = reservation["Instances"]
    for instance in instances:
        instance_ids_paris.append(instance['InstanceId'])
print("Done!")

response_paris = ec2_resource_paris.create_tags(
    Resources=instance_ids_paris,
    Tags=[
        {
            'Key': 'Env',
            'Value': 'dev'
        },
    ]
)