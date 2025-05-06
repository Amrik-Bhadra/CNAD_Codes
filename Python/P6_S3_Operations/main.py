import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# Initialize S3 client
s3 = boto3.client('s3', region_name='ap-south-1')

def create_bucket(bucket_name):
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': 'ap-south-1'
            }
        )
        print(f"Bucket '{bucket_name}' created successfully.")
    except ClientError as e:
        print(f"Error: {e}")

def upload_file(bucket_name, file_path, object_name):
    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"File '{file_path}' uploaded as '{object_name}'.")
    except FileNotFoundError:
        print("File not found.")
    except NoCredentialsError:
        print("AWS credentials not found.")

def list_objects(bucket_name):
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            print("Files in bucket:")
            for obj in response['Contents']:
                print(" -", obj['Key'])
        else:
            print("Bucket is empty.")
    except ClientError as e:
        print(f"Error: {e}")

def download_file(bucket_name, object_name, download_path):
    try:
        s3.download_file(bucket_name, object_name, download_path)
        print(f"File '{object_name}' downloaded to '{download_path}'.")
    except ClientError as e:
        print(f"Error: {e}")

def delete_file(bucket_name, object_name):
    try:
        s3.delete_object(Bucket=bucket_name, Key=object_name)
        print(f"File '{object_name}' deleted from bucket.")
    except ClientError as e:
        print(f"Error: {e}")

def delete_bucket(bucket_name):
    try:
        s3.delete_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' deleted.")
    except ClientError as e:
        print(f"Error: {e}")

# Menu-driven interface
def main():
    while True:
        print("\n--- AWS S3 Operations ---")
        print("1. Create Bucket")
        print("2. Upload File")
        print("3. List Files in Bucket")
        print("4. Download File")
        print("5. Delete File")
        print("6. Delete Bucket")
        print("7. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            bucket = input("Enter bucket name: ")
            create_bucket(bucket)
        elif choice == '2':
            bucket = input("Enter bucket name: ")
            file_path = input("Enter path to local file: ")
            object_name = input("Enter object name in S3: ")
            upload_file(bucket, file_path, object_name)
        elif choice == '3':
            bucket = input("Enter bucket name: ")
            list_objects(bucket)
        elif choice == '4':
            bucket = input("Enter bucket name: ")
            object_name = input("Enter object name to download: ")
            download_path = input("Enter local download path: ")
            download_file(bucket, object_name, download_path)
        elif choice == '5':
            bucket = input("Enter bucket name: ")
            object_name = input("Enter object name to delete: ")
            delete_file(bucket, object_name)
        elif choice == '6':
            bucket = input("Enter bucket name: ")
            delete_bucket(bucket)
        elif choice == '7':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
