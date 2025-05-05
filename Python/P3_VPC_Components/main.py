import boto3
region_name = 'ap-south-1'
ec2_client = boto3.client('ec2', region_name)

# create vpc
def create_vpc(cidr_block, vpc_name):
    vpc = ec2_client.create_vpc(
        CidrBlock=cidr_block
    )
    
    vpcId = vpc['Vpc']['VpcId']
    ec2_client.create_tags(Resources=[vpcId], Tags=[{'Key': 'Name', 'Value': vpc_name}])
    print(f"VPC Created! Id: {vpcId}")
    
    return vpcId


# create public subnet
def create_subnet(vpc_id, az, cidr_block, subnet_name):
    subnet = ec2_client.create_subnet(
        VpcId=vpc_id,
        CidrBlock=cidr_block,
        AvailabilityZone=az
    )
    
    subnet_id = subnet['Subnet']['SubnetId']
    ec2_client.create_tags(Resources=[subnet_id], Tags=[{'Key': 'Name', 'Value':subnet_name}])
    return subnet_id


# create internet gateway
def create_internet_gateway(igtw_name, vpc_id):
    igtw = ec2_client.create_internet_gateway()
    igtw_id = igtw['InternetGateway']['InternetGatewayId']
    ec2_client.create_tags(Resources=[igtw_id], Tags=[{'Key': 'Name', 'Value': igtw_name}])
    
    ec2_client.attach_internet_gateway(
        InternetGatewayId=igtw_id,
        VpcId=vpc_id
    )
    
    print(f"Internet Gateway Created! Id: {igtw_id}")
    return igtw_id


# create route table
def create_route_table(rt_table_name, vpc_id, igtw_id):
    rt_table = ec2_client.create_route_table(VpcId=vpc_id)
    rt_table_id = rt_table['RouteTable']['RouteTableId']
    ec2_client.create_tags(Resources=[rt_table_id], Tags=[{'Key': 'Name', 'Value': rt_table_name}])
    print(f"Route Table Created! Id: {rt_table_id}")
    
    # create route to igtw
    ec2_client.create_route(
        RouteTableId=rt_table_id,
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=igtw_id
    )
    
    return rt_table_id


# associate subnet with route table
def associate_route_table(rt_table_id, public_subnet_id):
    association = ec2_client.associate_route_table(
        RouteTableId=rt_table_id,
        SubnetId=public_subnet_id
    )
    
    print(f"Route table (id: {rt_table_id}) associated with subnet (id: {public_subnet_id})")
    
    return association['AssociationId']

# create security group
def create_security_group(vpc_id, sg_name, description):
    response = ec2_client.create_security_group(
        GroupName=sg_name,
        Description=description,
        VpcId=vpc_id
    )
    sg_id = response['GroupId']
    print(f"Security Group created: {sg_id}")
    
    # Allow SSH (port 22) from anywhere for testing purposes
    ec2_client.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }
        ]
    )
    return sg_id



# launch ec2 instance
def launch_instance(ami, key_pair, instance_type, maxCount, minCount, subnet_id, instance_name, security_group_id):
    response = ec2_client.run_instances(
        ImageId=ami,
        KeyName=key_pair,
        InstanceType=instance_type,
        MaxCount=maxCount,
        MinCount=minCount,
        SubnetId=subnet_id,
        SecurityGroupIds=[
            security_group_id,
        ],
        TagSpecifications=[
            {
                'ResourceType':'instance',
                'Tags':[
                    {
                        'Key':'Name',
                        'Value':instance_name
                    }
                ]
            }
        ]
        
    )
    
    instance_id = response['Instances'][0]['InstanceId']
    print(f"Launched EC2 instance in private subnet: {instance_id}")
    return instance_id
        



if __name__ == "__main__":
    # create vpc
    vpc_id = create_vpc('10.0.0.0/16', 'boto3_vpc')
    
    # get the azs
    azs = ec2_client.describe_availability_zones()['AvailabilityZones']
    az = azs[0]['ZoneName']
    
    # create public subnet
    public_subnet_id = create_subnet(vpc_id, az, '10.0.1.0/24', 'boto3_public_subnet')
    print(f"Public Subnet Created! ID: {public_subnet_id}")
    
    # create private subnet
    private_subnet_id = create_subnet(vpc_id, az, '10.0.2.0/24', 'boto3_private_subnet')
    print(f"Private Subnet Created! ID: {private_subnet_id}")
    
    # create igtw
    igtw_id = create_internet_gateway('boto_igtw', vpc_id)
    
    # create route table and create route to igtw
    rt_table_id = create_route_table('boto_rt_table', vpc_id, igtw_id)
    
    # associate route table with subnet - to connect it to igtw
    associationId = associate_route_table(rt_table_id, public_subnet_id)
    
    # Create Security Group in the same VPC
    security_group_id = create_security_group(vpc_id, 'boto3_sg', 'Allow SSH access')
    
    ami='ami-062f0cc54dbfd8ef1'
    key_pair='boto3_key_pair' 
    instance_type='t2.micro'
    maxCount = 1
    minCount = 1
    instance_name = 'boto_instance'
    
    # launch ec2.instance
    instanceId = launch_instance(ami, key_pair, instance_type, maxCount, minCount, private_subnet_id, instance_name, security_group_id)
    