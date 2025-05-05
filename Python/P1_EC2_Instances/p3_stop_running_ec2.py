import boto3
region_name = "ap-south-1"
ec2_client = boto3.client('ec2', region_name)

response = ec2_client.describe_instances(
    Filters=[{'Name': 'instance-state-name', 'Values':['running']}]
)

running_instances = []

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instanceId = instance['InstanceId']
        running_instances.append(instanceId)
        

if running_instances:
    print(f"Stopping the instances: {running_instances}")
    ec2_client.stop_instances(InstanceIds=running_instances)
else:
    print(f"No instances running")
        