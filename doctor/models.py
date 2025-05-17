from django.db import models
from django.contrib.auth import get_user_model
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError

User = get_user_model()



def certificate_upload_path(instance, filename):
    return f'doctor_certificates/{instance.application.user.id}/{filename}'

class DoctorApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_application')
    bio = models.TextField()
    specialization = models.CharField(max_length=100)
    certificates = models.FileField(upload_to=certificate_upload_path)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.status}"



class Certificate(models.Model):
    application = models.ForeignKey(DoctorApplication, related_name='certificate_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to=certificate_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificate for {self.application.user.email}"









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
    available_times = models.JSONField(default=dict)  # Format: {"Monday": [{"from": "09:00", "to": "4:00"}]}
    years_experience = models.PositiveIntegerField()
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doctor.firstname} {self.doctor.lastname} - {self.specialization}"

    def set_available_times(self, day, times):
        """
        Sets or replaces available time slots for a given day.
        Parameters:
        - day: string (e.g., 'Monday')
        - times: list of dicts (e.g., [{'from': '09:00', 'to': '12:00'}])
        """
        if day not in dict(self.DAYS_OF_WEEK):
            raise ValueError(f"{day} is not a valid day of the week.")
        if not isinstance(times, list):
            raise ValueError("Times must be a list of dictionaries with 'from' and 'to' keys.")
        for slot in times:
            if not isinstance(slot, dict) or 'from' not in slot or 'to' not in slot:
                raise ValueError("Each time slot must be a dictionary with 'from' and 'to' keys.")
        
        self.available_times[day] = times
        self.save()

    def get_available_times(self, day):
        """
        Returns a list of available time slots for a specific day, or an empty list if none set.
        """
        return self.available_times.get(day, [])

    def clean(self):
        """
        Ensure consistency between available_days and available_times.
        - No time slots should be provided for days not in available_days.
        """
        invalid_days = [day for day in self.available_times if day not in self.available_days]
        if invalid_days:
            raise ValidationError(
                f"The following days have time slots set but are not marked as available_days: {', '.join(invalid_days)}"
            )
