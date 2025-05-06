import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')

# -------------------- Create Table --------------------
def create_table():
    try:
        table = dynamodb.create_table(
            TableName='Students',
            KeySchema=[
                {'AttributeName': 'student_id', 'KeyType': 'HASH'}  # Partition key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'student_id', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        print("Creating table...")
        table.meta.client.get_waiter('table_exists').wait(TableName='Students')
        print("Table created successfully!")
    except ClientError as e:
        print("Error creating table:", e)

# -------------------- Insert Item --------------------
def insert_item():
    table = dynamodb.Table('Students')
    student_id = input("Enter student ID: ")
    name = input("Enter name: ")
    age = int(input("Enter age: "))

    table.put_item(
        Item={
            'student_id': student_id,
            'name': name,
            'age': age
        }
    )
    print("Item inserted successfully.")

# -------------------- Read Item --------------------
def read_item():
    table = dynamodb.Table('Students')
    student_id = input("Enter student ID to read: ")

    response = table.get_item(Key={'student_id': student_id})
    item = response.get('Item')

    if item:
        print("Item found:", item)
    else:
        print("Item not found.")

# -------------------- Update Item --------------------
def update_item():
    table = dynamodb.Table('Students')
    student_id = input("Enter student ID to update: ")
    new_age = int(input("Enter new age: "))

    response = table.update_item(
        Key={'student_id': student_id},
        UpdateExpression='SET age = :a',
        ExpressionAttributeValues={':a': new_age},
        ReturnValues='UPDATED_NEW'
    )
    print("Item updated:", response['Attributes'])

# -------------------- Delete Item --------------------
def delete_item():
    table = dynamodb.Table('Students')
    student_id = input("Enter student ID to delete: ")

    table.delete_item(Key={'student_id': student_id})
    print("Item deleted successfully.")

# -------------------- Delete Table --------------------
def delete_table():
    table = dynamodb.Table('Students')
    table.delete()
    print("Table deletion initiated...")

# -------------------- Main Menu --------------------
def main():
    while True:
        print("\nDynamoDB CRUD Operations")
        print("1. Create Table")
        print("2. Insert Item")
        print("3. Read Item")
        print("4. Update Item")
        print("5. Delete Item")
        print("6. Delete Table")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            create_table()
        elif choice == '2':
            insert_item()
        elif choice == '3':
            read_item()
        elif choice == '4':
            update_item()
        elif choice == '5':
            delete_item()
        elif choice == '6':
            delete_table()
        elif choice == '7':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
