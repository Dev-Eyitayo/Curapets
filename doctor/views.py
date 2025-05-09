# doctor_profile/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from .models import DoctorProfile
from .serializers import DoctorProfileSerializer

class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Only allow a doctor to create their own profile
        if self.request.user.role != 'doctor':
            raise PermissionDenied("Only doctors can create doctor profiles.")
        serializer.save(doctor=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.doctor != request.user:
            raise PermissionDenied("You can only update your own profile.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.doctor != request.user:
            raise PermissionDenied("You can only delete your own profile.")
        return super().destroy(request, *args, **kwargs)
