from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ['email', 'firstname', 'lastname', 'password', 'role']

    def create(self, validated_data):
       
        return CustomUser.objects.create_user(
            email=validated_data['email'],
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            password=validated_data['password'],
            role=validated_data.get('role', 'user')  
        )

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Get default token (with access and refresh)
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['firstname'] = user.firstname
        token['lastname'] = user.lastname
        token['role'] = user.role

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Optionally include additional user data in the response
        data.update({
            'email': self.user.email,
            'firstname': self.user.firstname,
            'lastname': self.user.lastname,
            'role': self.user.role,
        })

        return data
