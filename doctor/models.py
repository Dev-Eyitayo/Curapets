from django.db import models
from django.contrib.auth import get_user_model
from multiselectfield import MultiSelectField

User = get_user_model()

class DoctorProfile(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    doctor = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField()
    specialization = models.CharField(max_length=100)
    available_days = MultiSelectField(choices=DAYS_OF_WEEK)
    available_times = models.JSONField(default=list)  # Store as a list of time slots for each day
    years_experience = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doctor.get_full_name()} - {self.specialization}"

    def set_available_times(self, day, times):
        """
        Set available times for a given day. 
        Times should be a list of dictionaries with 'from' and 'to' times.
        Example: [{'from': '09:00', 'to': '12:00'}, {'from': '14:00', 'to': '17:00'}]
        """
        # Convert times to desired format (for validation or any custom handling)
        available_times = {day: times}
        self.available_times.append(available_times)  # Append to existing data

    def get_available_times(self, day):
        """
        Get available times for a specific day.
        """
        return [times for times in self.available_times if day in times]
