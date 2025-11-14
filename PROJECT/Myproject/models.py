from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, blank=True)
    # Link to Django's built-in User for proper authentication
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='student_profile')
    phone = models.CharField(max_length=15, blank=True)
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_id} - {self.name}"


class SSO(models.Model):
    """Student Service Officer model for SSO login and management."""
    sso_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, blank=True)
    # Optional link to a Django User account
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='sso_profile')
    phone = models.CharField(max_length=15, blank=True)
    office_location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sso_id} - {self.name}"


class Hostel(models.Model):
    name = models.CharField(max_length=100)
    total_rooms = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='hostels/')

    def __str__(self):
        return self.name

class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    number = models.PositiveIntegerField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.hostel.name} - Room {self.number}"


class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='complaints')
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.student_id} - {self.title}"


class Maintenance(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='maintenance_requests')
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.student_id} - {self.title}"


class Leave(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='leaves')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.student_id} - {self.start_date} to {self.end_date}"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[('present', 'Present'), ('absent', 'Absent'), ('leave', 'On Leave')],
        default='absent'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.student_id} - {self.date} ({self.status})"

