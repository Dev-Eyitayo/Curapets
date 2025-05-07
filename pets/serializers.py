from rest_framework import serializers
from .models import Pet

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'name', 'species', 'breed', 'age', 'image', 'owner', 'created_at']
        read_only_fields = ['id', 'created_at', 'owner']
