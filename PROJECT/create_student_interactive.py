"""
Interactive script to create new Student user IDs with details you fill in.
Run with the project's virtualenv Python:

C:/Users/Administrator/.virtualenvs/WebProject_Group03-ibWxYcE7/Scripts/python.exe c:/Users/Administrator/project/WebProject_Group03/PROJECT/create_student_interactive.py

The script will:
- Prompt you to enter number of students to create
- For each student, ask for: student_id, name, email, password, phone
- Create the Student records in the database
- Create Django User accounts linked to each Student
- Print a summary
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')
django.setup()

from django.contrib.auth.models import User
from Myproject.models import Student

created_students = []
created_users = []
errors = []

print("=" * 60)
print("Interactive Student User Creator")
print("=" * 60)

try:
    num_students = int(input("\nHow many new students do you want to create? "))
except ValueError:
    print("Invalid input. Exiting.")
    exit(1)

for i in range(num_students):
    print(f"\n--- Student {i + 1} of {num_students} ---")
    
    student_id = input(f"Enter Student ID (e.g., STU001): ").strip()
    if not student_id:
        print("  Skipped: Student ID is required.")
        continue
    
    # Check if student_id already exists
    if Student.objects.filter(student_id=student_id).exists():
        print(f"  Error: Student ID '{student_id}' already exists. Skipped.")
        errors.append(f"Student ID '{student_id}' already exists")
        continue
    
    name = input("Enter Name: ").strip()
    if not name:
        print("  Skipped: Name is required.")
        continue
    
    email = input("Enter Email: ").strip()
    if not email:
        print("  Skipped: Email is required.")
        continue
    
    # Check if email already exists
    if Student.objects.filter(email=email).exists():
        print(f"  Error: Email '{email}' already exists. Skipped.")
        errors.append(f"Email '{email}' already exists")
        continue
    
    password = input("Enter Password: ").strip()
    if not password:
        print("  Skipped: Password is required.")
        continue
    
    phone = input("Enter Phone (optional): ").strip()
    
    try:
        # Create Student
        student = Student.objects.create(
            student_id=student_id,
            name=name,
            email=email,
            password=password,
            phone=phone
        )
        created_students.append(student)
        print(f"  ✓ Created Student: {student_id} - {name}")
        
        # Create and link Django User
        try:
            user = User.objects.create_user(
                username=student_id,
                email=email,
                password=password,
                first_name=name
            )
            student.user = user
            student.save()
            created_users.append(user)
            print(f"  ✓ Created Django User: {student_id}")
        except Exception as e:
            print(f"  ⚠ Failed to create Django User: {e}")
            errors.append(f"Failed to create Django User for {student_id}: {e}")
    
    except Exception as e:
        print(f"  ✗ Failed to create student: {e}")
        errors.append(f"Failed to create student {student_id}: {e}")

print("\n" + "=" * 60)
print("Summary")
print("=" * 60)
print(f"Students created: {len(created_students)}")
print(f"Django Users created: {len(created_users)}")
if errors:
    print(f"\nErrors ({len(errors)}):")
    for error in errors:
        print(f"  - {error}")
else:
    print("No errors!")

if created_students:
    print("\nCreated Students:")
    for student in created_students:
        user_linked = "✓" if student.user else "✗"
        print(f"  [{user_linked}] {student.student_id} - {student.name} ({student.email})")

print("\nDone.")
