import pymysql

# Replace these with your actual RDS credentials
RDS_HOST = "your-rds-endpoint.amazonaws.com"
RDS_USER = "admin"
RDS_PASSWORD = "yourpassword"
RDS_DB = "school"

# Connect to the RDS MySQL DB
def connect():
    return pymysql.connect(
        host=RDS_HOST,
        user=RDS_USER,
        password=RDS_PASSWORD,
        database=RDS_DB
    )

# CREATE - Add a student
def create_student():
    conn = connect()
    cursor = conn.cursor()
    student_id = input("Enter student ID: ")
    name = input("Enter student name: ")
    age = int(input("Enter student age: "))

    try:
        cursor.execute("INSERT INTO students (student_id, name, age) VALUES (%s, %s, %s)", 
                       (student_id, name, age))
        conn.commit()
        print("Student added successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()

# READ - Get a student by ID
def read_student():
    conn = connect()
    cursor = conn.cursor()
    student_id = input("Enter student ID to read: ")
    
    try:
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        result = cursor.fetchone()
        if result:
            print("Student Record:", result)
        else:
            print("Student not found.")
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()

# UPDATE - Modify student's age
def update_student():
    conn = connect()
    cursor = conn.cursor()
    student_id = input("Enter student ID to update: ")
    new_age = int(input("Enter new age: "))
    
    try:
        cursor.execute("UPDATE students SET age = %s WHERE student_id = %s", (new_age, student_id))
        conn.commit()
        print("Student updated successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()

# DELETE - Remove a student
def delete_student():
    conn = connect()
    cursor = conn.cursor()
    student_id = input("Enter student ID to delete: ")
    
    try:
        cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        conn.commit()
        print("Student deleted successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()

# MENU
def main():
    while True:
        print("\nRDS MySQL - Student CRUD Operations")
        print("1. Add Student")
        print("2. Get Student")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")
        
        choice = input("Enter choice (1-5): ")
        
        if choice == '1':
            create_student()
        elif choice == '2':
            read_student()
        elif choice == '3':
            update_student()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
