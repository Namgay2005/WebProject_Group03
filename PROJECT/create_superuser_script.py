#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = 'kuenga'
email = 'kuenga@college.edu'
password = 'Kuenga@123'  # Temporary password - change after first login

if User.objects.filter(username=username).exists():
    print(f"User '{username}' already exists.")
else:
    try:
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Superuser '{username}' created with email '{email}'. Temporary password: {password}")
    except Exception as e:
        print('Failed to create superuser:', e)
