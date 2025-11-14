"""
Mark SSO-linked Django User accounts as staff (is_staff=True).
Run with the project's virtualenv Python:

C:/Users/Administrator/.virtualenvs/WebProject_Group03-ibWxYcE7/Scripts/python.exe c:/Users/Administrator/project/WebProject_Group03/PROJECT/mark_sso_staff.py

The script will:
- For each SSO record, ensure there is a linked User (try sso.user, else try to find User with username==sso.sso_id)
- Set user.is_staff = True and save
- Print a summary
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')
django.setup()

from django.contrib.auth.models import User
from Myproject.models import SSO

updated = 0
linked = 0
created_links = 0

for sso in SSO.objects.all():
    user = None
    if getattr(sso, 'user', None):
        user = sso.user
        linked += 1
    else:
        try:
            user = User.objects.get(username=sso.sso_id)
            # link it
            sso.user = user
            sso.save()
            created_links += 1
            linked += 1
            print(f"Linked existing User {user.username} to SSO {sso.sso_id}")
        except User.DoesNotExist:
            # Create a User if none exists so SSO can login via Django auth
            user = User.objects.create(username=sso.sso_id, email=sso.email, first_name=sso.name)
            if getattr(sso, 'password', None):
                try:
                    user.set_password(sso.password)
                except Exception:
                    user.set_unusable_password()
            else:
                user.set_unusable_password()
            user.is_staff = True
            user.save()
            sso.user = user
            sso.save()
            created_links += 1
            linked += 1
            updated += 1
            print(f"Created and linked User {user.username} and marked as staff for SSO {sso.sso_id}")

    if user:
        if not user.is_staff:
            user.is_staff = True
            user.save()
            updated += 1
            print(f"Marked User {user.username} as staff for SSO {sso.sso_id}")
        else:
            print(f"User {user.username} already staff for SSO {sso.sso_id}")
    else:
        print(f"No User found for SSO {sso.sso_id}; skipping")

print('\nSummary:')
print(f'  SSO records processed: {SSO.objects.count()}')
print(f'  Users linked during run: {created_links}')
print(f'  Users updated to staff: {updated}')
print('Done.')
