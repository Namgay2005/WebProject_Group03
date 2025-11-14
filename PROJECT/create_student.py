#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')
django.setup()

from Myproject.models import Student

# Create test student
student = Student.objects.create(
    student_id='STU001',
    name='John Doe',
    email='john@example.com',
    password='password123',
    phone='09261234567'
)
print(f"✓ Student created successfully: {student.name} ({student.student_id})")
