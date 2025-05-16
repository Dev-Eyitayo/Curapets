from rest_framework import serializers
from .models import Appointment, Pet
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

class AppointmentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    doctor = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.filter(role='doctor'))
    pet = serializers.PrimaryKeyRelatedField(queryset=Pet.objects.all())  # Ensure the pet exists

    class Meta:
        model = Appointment
        fields = ['id', 'pet', 'user', 'doctor', 'date', 'time', 'description', 'status', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        doctor = data['doctor']
        appointment_date = data['date']
        appointment_time = data['time']
        
        doctor_profile = doctor.profile
        available_times = doctor_profile.available_times
        weekday = appointment_date.strftime('%A')

        if weekday not in doctor_profile.available_days:
            raise serializers.ValidationError(f"Doctor is not available on {weekday}.")

        available_slots = available_times.get(weekday, [])
        
        if not available_slots:
            raise serializers.ValidationError(f"Doctor has no available time slots on {weekday}.")

        is_valid_time = False
        for slot in available_slots:
            if not isinstance(slot, dict) or 'from' not in slot or 'to' not in slot:
                raise serializers.ValidationError(f"Invalid time slot format: {slot}")
            
            slot_from = datetime.strptime(slot['from'], '%H:%M').time()
            slot_to = datetime.strptime(slot['to'], '%H:%M').time()

            if slot_from <= appointment_time <= slot_to:
                is_valid_time = True
                break

        if not is_valid_time:
            raise serializers.ValidationError(
                f"Selected time {appointment_time} is not within available slots on {weekday}."
            )

        return data

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
