import boto3

region_name = "ap-south-1"
ec2_client = boto3.client('ec2', region_name)

response = ec2_client.describe_instances(
    Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}]
)

stopped_instance_ids = []

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instanceId = instance['InstanceId']
        stopped_instance_ids.append(instanceId)
        

if stopped_instance_ids:
    print(f"Starting instances: {stopped_instance_ids}")
    ec2_client.start_instances(InstanceIds=stopped_instance_ids)
else:
    print("No stopped instances found")