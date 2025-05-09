from rest_framework import serializers
from .models import DoctorProfile

class DoctorProfileSerializer(serializers.ModelSerializer):
    doctor = serializers.ReadOnlyField(source='doctor.id')  # Automatically assign logged-in user

    class Meta:
        model = DoctorProfile
        fields = [
            'id', 'doctor', 'bio', 'specialization',
            'available_days', 'available_from', 'available_to',
            'years_experience', 'created_at'
        ]
        read_only_fields = ['id', 'doctor', 'created_at']
