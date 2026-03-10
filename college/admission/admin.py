from django.contrib import admin
from .models import Course, Student, Payment, Announcement, Document

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'duration', 'total_seats', 'available_seats', 'fee', 'is_active']
    list_filter = ['is_active', 'duration']
    search_fields = ['name', 'code']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'admission_number', 'course', 'application_status', 'application_date']
    list_filter = ['application_status', 'course', 'gender']
    search_fields = ['full_name', 'admission_number', 'user__email']
    readonly_fields = ['application_date', 'created_at', 'updated_at']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'amount', 'payment_date', 'transaction_id', 'status']
    list_filter = ['status', 'payment_method']
    search_fields = ['student__full_name', 'transaction_id', 'receipt_number']
    readonly_fields = ['payment_date']

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_date', 'expiry_date', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['student', 'document_type', 'uploaded_at', 'is_verified']
    list_filter = ['document_type', 'is_verified']
    search_fields = ['student__full_name']