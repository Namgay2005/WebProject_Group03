#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')
django.setup()

from Myproject.models import SSO

# Create test SSO
sso = SSO.objects.create(
    sso_id='SSO001',
    name='Tenzin Dorji',
    email='tenzin.sso@college.edu',
    password='sso12345',
    phone='09261234568',
    office_location='Office Building A'
)
print(f"✓ SSO created successfully: {sso.name} ({sso.sso_id})")
print(f"✓ Email: {sso.email}")
