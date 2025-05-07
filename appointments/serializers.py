from rest_framework import serializers
from .models import Appointment
from django.contrib.auth import get_user_model

User = get_user_model()

class AppointmentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    doctor = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.filter(role='doctor'))

    class Meta:
        model = Appointment
        fields = ['id', 'user', 'doctor', 'date', 'time', 'description', 'status', 'created_at']
        read_only_fields = ['created_at']

    def update(self, instance, validated_data):
        request_user = self.context['request'].user

        # Define what fields each role can update
        if request_user == instance.user:
            allowed_fields = {'date', 'time', 'description'}
        elif request_user == instance.doctor:
            allowed_fields = {'status'}
        else:
            raise serializers.ValidationError("You do not have permission to update this appointment.")

        # Reject any field not in allowed_fields
        for field in validated_data:
            if field not in allowed_fields:
                raise serializers.ValidationError(f"You cannot update the '{field}' field.")

        return super().update(instance, validated_data)
