# appointments/serializers.py

from rest_framework import serializers
from .models import Appointment
from django.contrib.auth import get_user_model

class AppointmentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    
    class Meta:
        model = Appointment
        fields = ['id', 'user', 'doctor', 'date', 'time', 'description', 'status', 'created_at']
        read_only_fields = ['created_at']

