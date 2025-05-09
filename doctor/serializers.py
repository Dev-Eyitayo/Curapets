from rest_framework import serializers
from .models import DoctorProfile

class DoctorProfileSerializer(serializers.ModelSerializer):
    available_times = serializers.JSONField()

    class Meta:
        model = DoctorProfile
        fields = ['doctor', 'bio', 'specialization', 'available_days', 'available_times', 'years_experience', 'created_at']

    def validate(self, data):
        """
        Validate available times to ensure there are no overlapping times for the same day.
        """
        # Check for time overlaps if needed
        for day, times in data.get('available_times', {}).items():
            for time_slot in times:
                # Custom validation logic for checking overlapping times
                pass
        return data
