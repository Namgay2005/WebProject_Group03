#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')
django.setup()

from Myproject.models import SSO

sso_id = 'SSO001'
new_name = 'Tshering Yangchey'

try:
    sso = SSO.objects.get(sso_id=sso_id)
    sso.name = new_name
    sso.save()
    print(f"Updated SSO {sso_id} to name: {new_name}")
except SSO.DoesNotExist:
    print(f"SSO with id {sso_id} does not exist. No changes made.")
except Exception as e:
    print('Error updating SSO:', e)
