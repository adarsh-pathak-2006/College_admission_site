from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator, FileExtensionValidator
import os

def document_upload_path(instance, filename):
    """Generate file path for uploaded documents"""
    ext = filename.split('.')[-1]
    filename = f"{instance.student.user.username}_document_{instance.id}.{ext}"
    return os.path.join('documents', filename)

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    duration = models.CharField(max_length=50)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    eligibility_criteria = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ['name']

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('WAITLISTED', 'Waitlisted')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name='students')
    
    # Personal Information
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?1?\d{9,15}$')])
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    
    # Academic Information
    previous_school = models.CharField(max_length=200)
    previous_grade = models.CharField(max_length=10)
    graduation_year = models.IntegerField()
    
    # Admission Details
    application_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    application_date = models.DateTimeField(auto_now_add=True)
    admission_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    
    # Documents
    marksheet_10th = models.FileField(upload_to=document_upload_path, validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])
    marksheet_12th = models.FileField(upload_to=document_upload_path, validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])
    photo = models.ImageField(upload_to=document_upload_path, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.admission_number}"

    class Meta:
        ordering = ['-application_date']

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded')
    ]
    
    PAYMENT_METHODS = [
        ('CARD', 'Credit/Debit Card'),
        ('UPI', 'UPI'),
        ('NETBANKING', 'Net Banking'),
        ('DEMAND_DRAFT', 'Demand Draft')
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')
    receipt_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    
    # For offline payments
    reference_number = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.transaction_id}"

    class Meta:
        ordering = ['-payment_date']

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date']

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('ID_PROOF', 'Identity Proof'),
        ('ADDRESS_PROOF', 'Address Proof'),
        ('EDUCATION', 'Educational Document'),
        ('OTHER', 'Other')
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='additional_documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_file = models.FileField(upload_to=document_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.document_type}"