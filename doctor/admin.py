# admin.py
from django.contrib import admin
from .models import DoctorProfile, DoctorApplication
from .admin_forms import DoctorProfileAdminForm

admin.site.register(DoctorApplication)
@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    form = DoctorProfileAdminForm
    list_display = ['doctor', 'specialization', 'years_experience', 'created_at']
    search_fields = ['doctor__firstname', 'doctor__lastname', 'specialization']
    list_filter = ['available_days', 'specialization']
