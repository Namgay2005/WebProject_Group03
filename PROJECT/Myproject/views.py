from django.shortcuts import render, redirect
from .models import Student, Complaint, Maintenance, Leave, Attendance, SSO
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta


def send_email_to_sso(subject, message, recipient_email=None):
    """Helper function to send emails to SSO.
    If no recipient_email provided, gets it from the SSO record in DB."""
    if recipient_email is None:
        try:
            sso = SSO.objects.first()  # Get the first (or primary) SSO
            if sso and sso.email:
                recipient_email = sso.email
            else:
                recipient_email = 'sso@college.edu'
        except Exception:
            recipient_email = 'sso@college.edu'
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email sending error: {e}")
        return False








def general_login(request):
    """Render the role selector page. If a POST with 'role' is received, redirect accordingly."""
    error_message = None

    if request.method == 'POST':
        role = request.POST.get('role')

        if role == 'student':
            return redirect('student_login')
        if role == 'sso':
            return redirect('sso_login')

        error_message = "Please select a role to continue."

    # reuse the existing choose_role template for role selection
    return render(request, 'choose_role.html', {'error_message': error_message})


def choose_role(request):
    return render(request, 'choose_role.html')


def student_login(request):
    """Authenticate student and redirect to dashboard on success."""
    error_message = None
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')
        
        # First try to authenticate via Django's auth (if a User exists)
        user = authenticate(request, username=student_id, password=password)
        if user is not None:
            # If user exists, prefer Django auth login
            auth_login(request, user)
            # Try to attach student info from related Student profile
            try:
                student = user.student_profile
                request.session['student_id'] = student.student_id
                request.session['student_name'] = student.name
                request.session['student_email'] = student.email
            except Exception:
                # Fall back to storing username
                request.session['student_id'] = user.username
                request.session['student_name'] = user.get_full_name() or user.username
                request.session['student_email'] = user.email
            return redirect('student_dashboard')

        # Fallback to legacy plaintext match for existing records (still supported)
        try:
            student = Student.objects.get(student_id=student_id, password=password)
            # Store student info in session
            request.session['student_id'] = student.student_id
            request.session['student_name'] = student.name
            request.session['student_email'] = student.email
            return redirect('student_dashboard')
        except Student.DoesNotExist:
            error_message = "Invalid Student ID or Password. Please try again."
    
    return render(request, 'student_login.html', {'error_message': error_message})


def student_dashboard(request):
    """Display student dashboard. Redirect to login if not authenticated."""
    # Check if student is logged in via session
    if 'student_id' not in request.session:
        return redirect('student_login')
    
    # Pass student info to template
    context = {
        'student_id': request.session.get('student_id'),
        'student_name': request.session.get('student_name'),
        'student_email': request.session.get('student_email'),
    }
    return render(request, 'student_dashboard.html', context)


def student_logout(request):
    """Log out student by clearing session."""
    # Clear Django auth session and regular session
    try:
        auth_logout(request)
    except Exception:
        pass
    request.session.flush()
    return redirect('student_login')


def index(request):
    """Homepage view."""
    return render(request, 'index.html')


def hostels(request):
    """Hostels page view."""
    return render(request, 'hostels.html')


def dechenling(request):
    """Dechenling hostel page view."""
    return render(request, 'dechenling.html')


def student_complaints(request):
    """Display and handle student complaints."""
    if 'student_id' not in request.session:
        return redirect('student_login')
    
    try:
        student = Student.objects.get(student_id=request.session['student_id'])
    except Student.DoesNotExist:
        return redirect('student_login')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title and description:
            complaint = Complaint.objects.create(
                student=student,
                title=title,
                description=description
            )
            
            # Send email to SSO
            subject = f"New Complaint from {student.name} ({student.student_id})"
            message = f"""
A new complaint has been submitted:

Student Name: {student.name}
Student ID: {student.student_id}
Email: {student.email}

Complaint Title: {title}
Description: {description}

Date: {complaint.created_at.strftime('%d %b %Y, %H:%M')}

Please address this complaint at your earliest convenience.
            """
            send_email_to_sso(subject, message)
            
            return redirect('student_complaints')
    
    complaints = Complaint.objects.filter(student=student).order_by('-created_at')
    context = {
        'student_name': request.session.get('student_name'),
        'complaints': complaints,
    }
    return render(request, 'student_complaints.html', context)


def student_maintenance(request):
    """Display and handle student maintenance requests."""
    if 'student_id' not in request.session:
        return redirect('student_login')
    
    try:
        student = Student.objects.get(student_id=request.session['student_id'])
    except Student.DoesNotExist:
        return redirect('student_login')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title and description:
            maintenance = Maintenance.objects.create(
                student=student,
                title=title,
                description=description
            )
            
            # Send email to SSO
            subject = f"New Maintenance Request from {student.name} ({student.student_id})"
            message = f"""
A new maintenance request has been submitted:

Student Name: {student.name}
Student ID: {student.student_id}
Email: {student.email}

Issue Title: {title}
Description: {description}

Date: {maintenance.created_at.strftime('%d %b %Y, %H:%M')}

Please process this maintenance request at your earliest convenience.
            """
            send_email_to_sso(subject, message)
            
            return redirect('student_maintenance')
    
    maintenance_requests = Maintenance.objects.filter(student=student).order_by('-created_at')
    context = {
        'student_name': request.session.get('student_name'),
        'maintenance_requests': maintenance_requests,
    }
    return render(request, 'student_maintenance.html', context)


def student_leave(request):
    """Display and handle student leave requests."""
    if 'student_id' not in request.session:
        return redirect('student_login')
    
    try:
        student = Student.objects.get(student_id=request.session['student_id'])
    except Student.DoesNotExist:
        return redirect('student_login')
    
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')
        if start_date and end_date and reason:
            leave = Leave.objects.create(
                student=student,
                start_date=start_date,
                end_date=end_date,
                reason=reason
            )
            
            # Send email to SSO
            subject = f"New Leave Request from {student.name} ({student.student_id})"
            message = f"""
A new leave request has been submitted:

Student Name: {student.name}
Student ID: {student.student_id}
Email: {student.email}

Leave Period: {start_date} to {end_date}
Reason: {reason}

Date Submitted: {leave.created_at.strftime('%d %b %Y, %H:%M')}

Please review and approve/reject this leave request.
            """
            send_email_to_sso(subject, message)
            
            return redirect('student_leave')
    
    leaves = Leave.objects.filter(student=student).order_by('-created_at')
    context = {
        'student_name': request.session.get('student_name'),
        'leaves': leaves,
    }
    return render(request, 'student_leave.html', context)


def student_attendance(request):
    """Display student attendance records."""
    if 'student_id' not in request.session:
        return redirect('student_login')
    
    try:
        student = Student.objects.get(student_id=request.session['student_id'])
    except Student.DoesNotExist:
        return redirect('student_login')
    
    # Get attendance records for the last 30 days
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    attendance_records = Attendance.objects.filter(
        student=student,
        date__gte=thirty_days_ago
    ).order_by('-date')
    
    # Calculate attendance statistics
    total_records = attendance_records.count()
    present_count = attendance_records.filter(status='present').count()
    absent_count = attendance_records.filter(status='absent').count()
    leave_count = attendance_records.filter(status='leave').count()
    
    attendance_percentage = (present_count / total_records * 100) if total_records > 0 else 0
    
    context = {
        'student_name': request.session.get('student_name'),
        'attendance_records': attendance_records,
        'total_records': total_records,
        'present_count': present_count,
        'absent_count': absent_count,
        'leave_count': leave_count,
        'attendance_percentage': round(attendance_percentage, 2),
    }
    return render(request, 'student_attendance.html', context)


# ===================== SSO Views =====================

def sso_login(request):
    """Authenticate SSO and redirect to SSO dashboard on success."""
    error_message = None
    
    if request.method == 'POST':
        sso_id = request.POST.get('sso_id')
        password = request.POST.get('password')
        # Try Django auth first if a User exists for this SSO
        user = authenticate(request, username=sso_id, password=password)
        if user is not None:
            auth_login(request, user)
            try:
                sso = user.sso_profile
                request.session['sso_id'] = sso.sso_id
                request.session['sso_name'] = sso.name
                request.session['sso_email'] = sso.email
            except Exception:
                request.session['sso_id'] = user.username
                request.session['sso_name'] = user.get_full_name() or user.username
                request.session['sso_email'] = user.email
            return redirect('sso_dashboard')

        # Fallback to legacy plaintext matching
        try:
            sso = SSO.objects.get(sso_id=sso_id, password=password)
            request.session['sso_id'] = sso.sso_id
            request.session['sso_name'] = sso.name
            request.session['sso_email'] = sso.email
            return redirect('sso_dashboard')
        except SSO.DoesNotExist:
            error_message = "Invalid SSO ID or Password. Please try again."
    
    return render(request, 'sso_login.html', {'error_message': error_message})


def sso_logout(request):
    """Log out SSO by clearing session."""
    try:
        auth_logout(request)
    except Exception:
        pass
    request.session.flush()
    return redirect('sso_login')


def sso_dashboard(request):
    """Display SSO dashboard. Redirect to login if not authenticated."""
    if 'sso_id' not in request.session:
        return redirect('sso_login')
    
    context = {
        'sso_name': request.session.get('sso_name'),
        'sso_id': request.session.get('sso_id'),
    }
    return render(request, 'sso_dashboard.html', context)


def sso_complaints(request):
    """SSO view all student complaints and update status."""
    if 'sso_id' not in request.session:
        return redirect('sso_login')
    
    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        status = request.POST.get('status')
        try:
            complaint = Complaint.objects.get(id=complaint_id)
            complaint.status = status
            complaint.save()
            
            # Send email to student about status update
            subject = f"Complaint Status Update - {complaint.title}"
            message = f"""
Dear {complaint.student.name},

Your complaint regarding "{complaint.title}" has been {status}.

Status: {complaint.get_status_display()}
Last Updated: {complaint.updated_at.strftime('%d %b %Y, %H:%M')}

Please contact SSO office if you need further assistance.
            """
            send_email_to_sso(subject, message, complaint.student.email)
        except Complaint.DoesNotExist:
            pass
    
    complaints = Complaint.objects.all().order_by('-created_at')
    context = {
        'sso_name': request.session.get('sso_name'),
        'complaints': complaints,
    }
    return render(request, 'sso_complaints.html', context)


def sso_maintenance(request):
    """SSO view all maintenance requests and approve/complete."""
    if 'sso_id' not in request.session:
        return redirect('sso_login')
    
    if request.method == 'POST':
        maintenance_id = request.POST.get('maintenance_id')
        status = request.POST.get('status')
        try:
            maintenance = Maintenance.objects.get(id=maintenance_id)
            maintenance.status = status
            maintenance.save()
            
            # Send email to student about status update
            subject = f"Maintenance Request Status Update - {maintenance.title}"
            message = f"""
Dear {maintenance.student.name},

Your maintenance request regarding "{maintenance.title}" has been {status}.

Status: {maintenance.get_status_display()}
Last Updated: {maintenance.updated_at.strftime('%d %b %Y, %H:%M')}

Please contact SSO office if you need further assistance.
            """
            send_email_to_sso(subject, message, maintenance.student.email)
        except Maintenance.DoesNotExist:
            pass
    
    maintenance_requests = Maintenance.objects.all().order_by('-created_at')
    context = {
        'sso_name': request.session.get('sso_name'),
        'maintenance_requests': maintenance_requests,
    }
    return render(request, 'sso_maintenance.html', context)


def sso_leave(request):
    """SSO view all leave requests and approve/reject."""
    if 'sso_id' not in request.session:
        return redirect('sso_login')
    
    if request.method == 'POST':
        leave_id = request.POST.get('leave_id')
        status = request.POST.get('status')
        try:
            leave = Leave.objects.get(id=leave_id)
            leave.status = status
            leave.save()
            
            # Send email to student about leave approval/rejection
            subject = f"Leave Request {leave.get_status_display()}"
            message = f"""
Dear {leave.student.name},

Your leave request has been {status.lower()}.

Leave Period: {leave.start_date} to {leave.end_date}
Reason: {leave.reason}
Status: {leave.get_status_display()}

Please contact SSO office if you have any questions.
            """
            send_email_to_sso(subject, message, leave.student.email)
        except Leave.DoesNotExist:
            pass
    
    leaves = Leave.objects.all().order_by('-created_at')
    context = {
        'sso_name': request.session.get('sso_name'),
        'leaves': leaves,
    }
    return render(request, 'sso_leave.html', context)


def sso_attendance(request):
    """SSO view student attendance records."""
    if 'sso_id' not in request.session:
        return redirect('sso_login')
    
    students = Student.objects.all()
    selected_student_id = request.GET.get('student_id')
    attendance_records = None
    
    if selected_student_id:
        try:
            student = Student.objects.get(id=selected_student_id)
            attendance_records = Attendance.objects.filter(student=student).order_by('-date')
        except Student.DoesNotExist:
            pass
    
    context = {
        'sso_name': request.session.get('sso_name'),
        'students': students,
        'selected_student_id': selected_student_id,
        'attendance_records': attendance_records,
    }
    return render(request, 'sso_attendance.html', context)

