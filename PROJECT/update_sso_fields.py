#!/usr/bin/env python
import os
import django

# Assumption: the new name should be "Wangmo Kuenga" (inferred from the email local-part)
NEW_NAME = 'Wangmo Kuenga'
NEW_EMAIL = 'wangmokuenga2004@gmail.com'
NEW_PHONE = '17000000'
SSO_ID = 'SSO001'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')
try:
    django.setup()
except Exception as e:
    print('Django setup error:', e)
    raise

from Myproject.models import SSO

try:
    sso = SSO.objects.get(sso_id=SSO_ID)
    sso.name = NEW_NAME
    sso.email = NEW_EMAIL
    sso.phone = NEW_PHONE
    sso.save()
    print(f"Updated SSO {SSO_ID}: name={NEW_NAME}, email={NEW_EMAIL}, phone={NEW_PHONE}")
except SSO.DoesNotExist:
    print(f"SSO with id {SSO_ID} does not exist.")
except Exception as e:
    print('Error updating SSO:', e)
