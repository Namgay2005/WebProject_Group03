#!/usr/bin/env python
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')
try:
    django.setup()
except Exception as e:
    print('Django setup error:', e)
    raise

from Myproject.models import SSO

ssos = SSO.objects.all()
if not ssos:
    print('No SSO records found in the database.')
else:
    print(f'Found {ssos.count()} SSO record(s):\n')
    for s in ssos:
        print('---')
        print(f'id: {s.id}')
        print(f'sso_id: {s.sso_id}')
        print(f'name: {s.name}')
        print(f'email: {s.email}')
        print(f'phone: {s.phone}')
        print(f'office_location: {s.office_location}')
        print(f'created_at: {s.created_at}')
        print('---\n')
