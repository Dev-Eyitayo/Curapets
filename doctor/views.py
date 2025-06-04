# doctor_profile/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from .models import DoctorProfile, DoctorApplication
from .serializers import DoctorProfileSerializer, DoctorApplicationSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError


User = get_user_model()

class DoctorApplicationViewSet(viewsets.ModelViewSet):
    queryset = DoctorApplication.objects.all()
    serializer_class = DoctorApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return DoctorApplication.objects.all()
        return DoctorApplication.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Check if the user already has a doctor application
        if DoctorApplication.objects.filter(user=self.request.user).exists():
            raise ValidationError("You have already submitted an application.")
        serializer.save(user=self.request.user)
   
    
    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("You cannot update a doctor application.")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("You cannot update a doctor application.")
        return super().partial_update(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def review(self, request, pk=None):
        application = self.get_object()
        status_value = request.data.get('status')

        if status_value not in ['approved', 'rejected']:
            return Response({"detail": "Invalid status."}, status=400)

        application.status = status_value
        application.save()

        if status_value == 'approved':
            application.user.role = 'doctor'
            application.user.save()

        return Response({"detail": f"Application {status_value} successfully."})





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
