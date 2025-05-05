import boto3
region_name = 'ap-south-1'
ec2_client = boto3.client('ec2', region_name)

response = ec2_client.describe_instances(
    Filters = [{'Name':'instance-state-name', 'Values':['running', 'stopped']}]
)

instance_ids = []

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        id = instance['InstanceId']
        instance_ids.append(id)
        

if instance_ids:
    print(f"Terminating the instances: {instance_ids}")
    ec2_client.terminate_instances(InstanceIds=instance_ids)
    
else:
    print("No instance available")

