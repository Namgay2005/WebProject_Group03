"""
Script to create Django User accounts for existing Student and SSO records and link them.
Run from project root with the project's virtualenv active:

python PROJECT\create_auth_users.py

This script will:
- Create a Django User with username equal to student.student_id (or sso.sso_id) if not present
- Use the existing plaintext password for the initial set_password (so users can login via Django auth)
- Link the created User to the Student/SSO.user field
- Print a summary

WARNING: This script uses plaintext passwords that exist in the Student/SSO.password fields. After running, you should delete or clear those plaintext password fields and ensure proper password reset flows.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')
django.setup()

from django.contrib.auth.models import User
from Myproject.models import Student, SSO

created = 0
skipped = 0

print('Starting creation of Django User accounts for Student and SSO records...')

# Students
for student in Student.objects.all():
    username = student.student_id
    if student.user:
        print(f"Student {username}: already linked to User {student.user.username}")
        skipped += 1
        continue
    # If a User with that username exists, link it
    user, was_created = User.objects.get_or_create(username=username, defaults={
        'email': student.email,
        'first_name': student.name,
    })
    if was_created:
        # Set password from the legacy field if present, otherwise use a random unusable password
        if student.password:
            user.set_password(student.password)
        else:
            user.set_unusable_password()
        user.save()
        print(f"Created User for Student {username}")
        created += 1
    else:
        print(f"Found existing User {user.username} for Student {username}; linking")
    student.user = user
    student.save()

# SSO
for sso in SSO.objects.all():
    username = sso.sso_id
    if sso.user:
        print(f"SSO {username}: already linked to User {sso.user.username}")
        skipped += 1
        continue
    user, was_created = User.objects.get_or_create(username=username, defaults={
        'email': sso.email,
        'first_name': sso.name,
    })
    if was_created:
        if sso.password:
            user.set_password(sso.password)
        else:
            user.set_unusable_password()
        user.save()
        print(f"Created User for SSO {username}")
        created += 1
    else:
        print(f"Found existing User {user.username} for SSO {username}; linking")
    sso.user = user
    sso.save()

print('\nDone. Summary:')
print(f'  Created Users: {created}')
print(f'  Skipped (already linked): {skipped}')
print('NOTE: Remove plaintext password fields from Student and SSO models and database after verifying login works.')
