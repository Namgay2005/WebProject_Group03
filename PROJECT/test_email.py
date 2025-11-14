"""
Test Gmail email configuration directly.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("Testing Gmail email configuration...")
print("=" * 60)
print(f"Email Backend: {settings.EMAIL_BACKEND}")
print(f"Email Host: {settings.EMAIL_HOST}")
print(f"Email Port: {settings.EMAIL_PORT}")
print(f"Email Use TLS: {settings.EMAIL_USE_TLS}")
print(f"Email Host User: {settings.EMAIL_HOST_USER}")
print(f"Default From Email: {settings.DEFAULT_FROM_EMAIL}")
print("=" * 60)

try:
    result = send_mail(
        subject='Test Email from Django',
        message='This is a test email to verify Gmail is working.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['wangmokuenga2004@gmail.com'],
        fail_silently=False,
    )
    print(f"✓ Email sent successfully! Result: {result}")
except Exception as e:
    print(f"✗ Email failed to send!")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {e}")
    import traceback
    traceback.print_exc()
