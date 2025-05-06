import json
import boto3

def lambda_handler(event, context):
    # Extract the bucket name and the key (file name) from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Initialize the S3 client
    s3_client = boto3.client('s3')
    
    # Retrieve the object metadata from the S3 bucket
    response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
    
    # Display object details
    print(f"Bucket Name: {bucket_name}")
    print(f"Object Key: {object_key}")
    print(f"Object Size: {response['ContentLength']} bytes")
    print(f"Last Modified: {response['LastModified']}")
    print(f"Content Type: {response['ContentType']}")
    
    # Optionally, you can read the file's content if needed (e.g., for text files)
    # file_content = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    # print("File Content:", file_content['Body'].read().decode('utf-8'))
    
    return {
        'statusCode': 200,
        'body': json.dumps(f"Details of object {object_key} from bucket {bucket_name} fetched successfully")
    }
