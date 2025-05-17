from rest_framework.routers import DefaultRouter
from .views import DoctorProfileViewSet, DoctorApplicationViewSet

router = DefaultRouter()

router.register('applications', DoctorApplicationViewSet, basename='doctor-application')
router.register(r'doctor-profiles', DoctorProfileViewSet, basename='doctor-profile')

urlpatterns = router.urls
