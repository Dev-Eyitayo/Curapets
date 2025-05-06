from rest_framework import generics
from .models import CustomUser
from .serializers import SignUpSerializer
from rest_framework.permissions import AllowAny




class SignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]
    
    

