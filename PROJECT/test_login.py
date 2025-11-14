"""
Quick test to verify student login works with newly created students.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')
django.setup()

from Myproject.models import Student
from django.contrib.auth import authenticate

print("Testing student login with newly created students...")
print("=" * 60)

# Test with the first imported student
test_student_id = '08230103'
test_password = 'password123'

# Check if student exists in DB
student = Student.objects.filter(student_id=test_student_id).first()
if student:
    print(f"✓ Found Student: {student.student_id} - {student.name}")
    print(f"  Email: {student.email}")
    print(f"  Has Django User: {'Yes' if student.user else 'No'}")
    
    # Test Django auth
    if student.user:
        user = authenticate(username=test_student_id, password=test_password)
        if user:
            print(f"✓ Django auth works: {user.username} authenticated successfully")
        else:
            print(f"✗ Django auth failed for username={test_student_id}")
    
    # Test legacy plaintext
    if student.password == test_password:
        print(f"✓ Legacy plaintext password matches")
    else:
        print(f"✗ Legacy plaintext password does NOT match (stored: {student.password[:20]}...)")
else:
    print(f"✗ Student {test_student_id} not found in database")

print("\n" + "=" * 60)
print(f"Total Students in DB: {Student.objects.count()}")
print("Sample of created students:")
for s in Student.objects.all()[:5]:
    print(f"  - {s.student_id}: {s.name} (user: {'✓' if s.user else '✗'})")
