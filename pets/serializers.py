from rest_framework import serializers
from pets.models import Pet

class PetSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(min_value=0)
    class Meta:
        model = Pet
        fields = ['id', 'name', 'species', 'breed', 'age', 'image', 'created_at', 'owner']
        read_only_fields = ['owner', 'created_at']
