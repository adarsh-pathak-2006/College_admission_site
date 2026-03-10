import os
import uuid
from django.utils import timezone
import random

def generate_unique_id(prefix=''):
    """Generate a unique ID"""
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    random_part = random.randint(1000, 9999)
    return f"{prefix}{timestamp}{random_part}"

def handle_uploaded_file(file, destination):
    """Handle file upload"""
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, 'wb+') as destination_file:
        for chunk in file.chunks():
            destination_file.write(chunk)

def get_file_extension(filename):
    """Get file extension"""
    return os.path.splitext(filename)[1].lower()

def is_valid_file_extension(filename, allowed_extensions):
    """Check if file extension is allowed"""
    ext = get_file_extension(filename)
    return ext in allowed_extensions