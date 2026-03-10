from django.conf import settings

def site_settings(request):
    """Context processor to add site-wide settings to templates"""
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'College Admission System'),
        'SITE_DESCRIPTION': getattr(settings, 'SITE_DESCRIPTION', 'Your gateway to quality education'),
        'CONTACT_PHONE': getattr(settings, 'CONTACT_PHONE', '+1 234 567 890'),
        'CONTACT_ADDRESS': getattr(settings, 'CONTACT_ADDRESS', '123 College Street'),
        'CURRENT_ACADEMIC_YEAR': getattr(settings, 'CURRENT_ACADEMIC_YEAR', '2024-2025'),
        'APPLICATION_FEE': getattr(settings, 'APPLICATION_FEE', 1000),
    }