from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Student, Course, Payment, Announcement
import datetime

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user', 'application_status', 'admission_number', 'created_at', 'updated_at']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'previous_school': forms.TextInput(attrs={'class': 'form-control'}),
            'previous_grade': forms.TextInput(attrs={'class': 'form-control'}),
            'graduation_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'marksheet_10th': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.jpg,.jpeg,.png'}),
            'marksheet_12th': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.jpg,.jpeg,.png'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png'}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'reference_number']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'reference_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Transaction/Reference number'}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'total_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'available_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'eligibility_criteria': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'expiry_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }