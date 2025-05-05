import boto3;

region_name = "ap-south-1"
ec2_client = boto3.client('ec2', region_name)

response = ec2_client.describe_instances()

# print(response)

state_counts = {
    'running': 0,
    'stopped': 0,
    'terminated': 0,
}

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        state = instance['State']['Name']
        if state in state_counts:
            state_counts[state] += 1
            
            
print(f"Number of instances running: {state_counts['running']}")
print(f"Number of instances stopped: {state_counts['stopped']}")
print(f"Number of instances terminated: {state_counts['terminated']}")