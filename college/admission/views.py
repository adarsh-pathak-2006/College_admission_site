from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from django.utils import timezone
from .models import *
from .forms import *
from .decorators import admin_required
import uuid
import random

def home(request):
    """Home page view"""
    announcements = Announcement.objects.filter(
        is_active=True, 
        expiry_date__gte=timezone.now().date()
    )[:5]
    courses = Course.objects.filter(is_active=True)[:4]
    
    context = {
        'announcements': announcements,
        'courses': courses,
        'total_students': Student.objects.count(),
        'total_courses': Course.objects.count(),
    }
    return render(request, 'admission/home.html', context)

def register(request):
    """Student registration view"""
    if request.method == 'POST':
        user_form = StudentRegistrationForm(request.POST)
        profile_form = StudentProfileForm(request.POST, request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Create user
            user = user_form.save()
            
            # Create student profile
            student = profile_form.save(commit=False)
            student.user = user
            student.admission_number = generate_admission_number()
            student.save()
            
            messages.success(request, 'Registration successful! Please login to continue.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = StudentRegistrationForm()
        profile_form = StudentProfileForm()
    
    courses = Course.objects.filter(is_active=True)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'courses': courses
    }
    return render(request, 'admission/register.html', context)

def login_view(request):
    """Login view"""
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        else:
            return redirect('student_dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                
                if user.is_staff or user.is_superuser:
                    return redirect('admin_dashboard')
                else:
                    return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'admission/login.html', {'form': form})

@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def student_dashboard(request):
    """Student dashboard view"""
    try:
        student = request.user.student_profile
        payments = student.payments.all().order_by('-payment_date')[:5]
        total_paid = student.payments.filter(status='COMPLETED').aggregate(Sum('amount'))['amount__sum'] or 0
        
        context = {
            'student': student,
            'payments': payments,
            'total_paid': total_paid,
            'pending_fee': student.course.fee - total_paid if student.course else 0,
        }
        return render(request, 'admission/student_dashboard.html', context)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('home')

@login_required
def payment_view(request):
    """Fee payment view"""
    try:
        student = request.user.student_profile
        
        if request.method == 'POST':
            form = PaymentForm(request.POST)
            if form.is_valid():
                payment = form.save(commit=False)
                payment.student = student
                payment.amount = student.course.fee
                payment.transaction_id = generate_transaction_id()
                payment.receipt_number = generate_receipt_number()
                payment.save()
                
                messages.success(request, 'Payment initiated successfully. Please complete the payment.')
                return redirect('payment_status', payment_id=payment.id)
        else:
            form = PaymentForm()
        
        context = {
            'student': student,
            'form': form,
            'course_fee': student.course.fee if student.course else 0,
        }
        return render(request, 'admission/payment.html', context)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('home')

@login_required
def payment_status(request, payment_id):
    """Payment status view"""
    payment = get_object_or_404(Payment, id=payment_id, student=request.user.student_profile)
    return render(request, 'admission/payment_status.html', {'payment': payment})

@login_required
@admin_required
def admin_dashboard(request):
    """Admin dashboard view"""
    total_students = Student.objects.count()
    pending_applications = Student.objects.filter(application_status='PENDING').count()
    total_payments = Payment.objects.filter(status='COMPLETED').aggregate(Sum('amount'))['amount__sum'] or 0
    total_courses = Course.objects.count()
    recent_applications = Student.objects.all().order_by('-application_date')[:10]
    
    context = {
        'total_students': total_students,
        'pending_applications': pending_applications,
        'total_payments': total_payments,
        'total_courses': total_courses,
        'recent_applications': recent_applications,
    }
    return render(request, 'admission/admin_dashboard.html', context)

@login_required
@admin_required
def manage_applications(request):
    """Manage student applications"""
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '')
    
    applications = Student.objects.all()
    
    if status_filter != 'all':
        applications = applications.filter(application_status=status_filter)
    
    if search_query:
        applications = applications.filter(
            Q(full_name__icontains=search_query) |
            Q(admission_number__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )
    
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'applications': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    return render(request, 'admission/applications_review.html', context)

@login_required
@admin_required
def update_application_status(request, student_id):
    """Update student application status"""
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        student.application_status = new_status
        student.save()
        messages.success(request, f'Application status updated to {new_status}')
    
    return redirect('manage_applications')

@login_required
@admin_required
def manage_courses(request):
    """Manage courses"""
    courses = Course.objects.all()
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course added successfully!')
            return redirect('manage_courses')
    else:
        form = CourseForm()
    
    context = {
        'courses': courses,
        'form': form,
    }
    return render(request, 'admission/manage_courses.html', context)

@login_required
@admin_required
def edit_course(request, course_id):
    """Edit course"""
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('manage_courses')
    else:
        form = CourseForm(instance=course)
    
    context = {
        'form': form,
        'course': course,
    }
    return render(request, 'admission/edit_course.html', context)

@login_required
@admin_required
def delete_course(request, course_id):
    """Delete course"""
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
    return redirect('manage_courses')

def generate_admission_number():
    """Generate unique admission number"""
    year = timezone.now().year
    random_num = random.randint(1000, 9999)
    return f"ADM{year}{random_num}"

def generate_transaction_id():
    """Generate unique transaction ID"""
    return f"TXN{timezone.now().strftime('%Y%m%d%H%M%S')}{random.randint(100,999)}"

def generate_receipt_number():
    """Generate unique receipt number"""
    return f"RCP{timezone.now().strftime('%Y%m%d%H%M%S')}{random.randint(10,99)}"