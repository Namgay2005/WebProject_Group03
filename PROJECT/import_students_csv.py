"""
Import Student users from a CSV file.
Run with the project's virtualenv Python:

C:/Users/Administrator/.virtualenvs/WebProject_Group03-ibWxYcE7/Scripts/python.exe c:/Users/Administrator/project/WebProject_Group03/PROJECT/import_students_csv.py

The script will:
- Read students_import.csv from the PROJECT folder
- Create Student records for each row
- Create linked Django User accounts
- Print a summary with success/error counts
"""
import os
import csv
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')
django.setup()

from django.contrib.auth.models import User
from Myproject.models import Student

csv_file = os.path.join(os.path.dirname(__file__), 'students_import.csv')

if not os.path.exists(csv_file):
    print(f"Error: {csv_file} not found.")
    exit(1)

created_students = []
created_users = []
errors = []

print("=" * 60)
print("CSV Student Importer")
print("=" * 60)
print(f"Reading from: {csv_file}\n")

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    # Strip whitespace from fieldnames and values
    if reader.fieldnames:
        reader.fieldnames = [name.strip() for name in reader.fieldnames]
    for row_num, row in enumerate(reader, start=2):  # start=2 because row 1 is headers
        # Strip keys and values
        row = {k.strip(): v.strip() for k, v in row.items()}
        student_id = row.get('student_id', '').strip()
        name = row.get('name', '').strip()
        email = row.get('email', '').strip()
        password = row.get('password', '').strip()
        phone = row.get('phone', '').strip()

        if not student_id or not name or not email or not password:
            errors.append(f"Row {row_num}: Missing required fields (student_id, name, email, password)")
            continue

        # Check for duplicates
        if Student.objects.filter(student_id=student_id).exists():
            errors.append(f"Row {row_num}: Student ID '{student_id}' already exists")
            continue

        if Student.objects.filter(email=email).exists():
            errors.append(f"Row {row_num}: Email '{email}' already exists")
            continue

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
                print(f"✓ Created: {student_id} - {name}")
            except Exception as e:
                print(f"⚠ Row {row_num}: Student created but Django User failed: {e}")
                errors.append(f"Row {row_num}: Django User creation failed for {student_id}: {e}")

        except Exception as e:
            errors.append(f"Row {row_num}: Failed to create student: {e}")
            print(f"✗ Row {row_num}: {e}")

print("\n" + "=" * 60)
print("Summary")
print("=" * 60)
print(f"Students created: {len(created_students)}")
print(f"Django Users created: {len(created_users)}")

if errors:
    print(f"\nErrors/Warnings ({len(errors)}):")
    for error in errors:
        print(f"  - {error}")
else:
    print("\nAll rows imported successfully!")

print("\nDone.")
