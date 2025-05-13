from rest_framework import serializers
from .models import DoctorProfile
import datetime

class DoctorProfileSerializer(serializers.ModelSerializer):
    available_times = serializers.JSONField()

    class Meta:
        model = DoctorProfile
        fields = [
            'doctor', 'bio', 'specialization',
            'available_days', 'available_times',
            'years_experience', 'created_at'
        ]
        read_only_fields = ['created_at']

    def validate_available_times(self, value):
        DAYS_OF_WEEK = dict(DoctorProfile.DAYS_OF_WEEK)

        if not isinstance(value, dict):
            raise serializers.ValidationError("available_times must be a dictionary with days as keys.")

        for day, time_slots in value.items():
            if day not in DAYS_OF_WEEK:
                raise serializers.ValidationError(f"'{day}' is not a valid day of the week.")

            if not isinstance(time_slots, list):
                raise serializers.ValidationError(f"Time slots for {day} must be a list.")

            for slot in time_slots:
                if not isinstance(slot, dict) or 'from' not in slot or 'to' not in slot:
                    raise serializers.ValidationError(
                        f"Each time slot for {day} must be a dict with 'from' and 'to' keys."
                    )
                try:
                    from_time = datetime.datetime.strptime(slot['from'], "%H:%M").time()
                    to_time = datetime.datetime.strptime(slot['to'], "%H:%M").time()
                except ValueError:
                    raise serializers.ValidationError(
                        f"Time format for {day} must be 'HH:MM'. Got: {slot}"
                    )
                if from_time >= to_time:
                    raise serializers.ValidationError(
                        f"'from' time must be earlier than 'to' time on {day}."
                    )

            # Check for overlapping slots
            sorted_slots = sorted(
                [
                    (
                        datetime.datetime.strptime(slot['from'], "%H:%M").time(),
                        datetime.datetime.strptime(slot['to'], "%H:%M").time()
                    )
                    for slot in time_slots
                ],
                key=lambda x: x[0]
            )

            for i in range(1, len(sorted_slots)):
                prev_end = sorted_slots[i - 1][1]
                curr_start = sorted_slots[i][0]
                if curr_start < prev_end:
                    raise serializers.ValidationError(
                        f"Overlapping time slots found on {day}."
                    )

        return value

    def validate(self, data):
        """
        Ensure available_times only includes days in available_days.
        """
        available_days = data.get('available_days', [])
        available_times = data.get('available_times', {})

        invalid_days = [day for day in available_times if day not in available_days]
        if invalid_days:
            raise serializers.ValidationError({
                "available_times": f"Time slots set for days not in available_days: {', '.join(invalid_days)}"
            })

        return data
