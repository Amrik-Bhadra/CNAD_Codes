import boto3
import json  # convert to json format

region_name = 'ap-south-1'

iam_client = boto3.client('iam')

# create_user
def createUser(username):
    return iam_client.create_user(UserName=username)

# list_users
def listUsers():
    allUsersResponse = iam_client.list_users()
    users = []
    for user in allUsersResponse['Users']:
        users.append(user['UserName'])
        
    return users

# delete_user
def deleteUser(username):
    try:
        return iam_client.delete_user(UserName=username)
    except iam_client.exceptions.NoSuchEntityException:
        print(f"User {username} Not Found!")
        return None


# create policy
def createPolicy(policyName, policyDocument):
    return iam_client.create_policy(
        PolicyName=policyName,
        PolicyDocument=policyDocument
    )
    
# create user
def createGroup(groupName):
    try:
        return iam_client.create_group(
            GroupName=groupName
        )
    except iam_client.exceptions.EntityAlreadyExistsException:
        print(f"Group '{groupName}' already exists.")
        return None
    except Exception as e:
        print(f"Error creating group: {e}")
        return None


# attach user policy
def attachUserPolicy(username, policyArn):
    try:
        return iam_client.attach_user_policy(
            UserName=username,
            PolicyArn=policyArn
        )
    except iam_client.exceptions.NoSuchEntityException:
        print(f"User '{username}' or policy '{policyArn}' does not exist.")
        return None
    except Exception as e:
        print(f"Error attaching policy to user: {e}")
        return None
        


if __name__ == "__main__":
    policyArn = ""

    while True:
        print('\nIAM operations:')
        print('1. Create User')
        print('2. Delete User')
        print('3. List all users')
        print('4. Create policy')
        print('5. Create Group')
        print('6. Attach Policy to User')
        print('7. Exit')
        
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        match choice:
            case 1:
                username = input("Enter a username: ")
                response = createUser(username)
                print(f"User created successfully! UserId: {response['User']['UserId']}")

            case 2:
                username = input("Enter a username to delete: ")
                response = deleteUser(username)
                if response:
                    print(f"User {username} deleted")

            case 3:
                response = listUsers()
                if response:
                    print(f"All users are: {response}")
                else:
                    print("No users")

            case 4:
                policyName = input("Enter policy name: ")
                policyDocument = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "S3FullAccess",
                            "Effect": "Allow",
                            "Action": "s3:*",
                            "Resource": "*"
                        },
                        {
                            "Sid": "EC2ReadOnlyAccess",
                            "Effect": "Allow",
                            "Action": [
                                "ec2:Describe*",
                                "ec2:GetConsoleOutput",
                                "ec2:GetPasswordData"
                            ],
                            "Resource": "*"
                        }
                    ]
                }
                response = createPolicy(policyName, json.dumps(policyDocument))
                if response:
                    print(f"Policy created! ID: {response['Policy']['PolicyId']}")
                    policyArn = response['Policy']['Arn']
                else:
                    print("Policy not created!")

            case 5:
                groupName = input("Enter a group name: ")
                response = createGroup(groupName)
                if response:
                    print(f"Group Created! ID: {response['Group']['GroupId']}")
                else:
                    print("Group Not Created!")

            case 6:
                username = input("Enter username: ")
                if policyArn:
                    response = attachUserPolicy(username, policyArn)
                    if response:
                        print(f"Policy {policyArn} attached to {username}")
                else:
                    print("No policy created or loaded yet. Please create one first.")

            case 7:
                print("Exiting program.")
                break

            case _:
                print("Invalid choice. Please select a valid option.")

        
            