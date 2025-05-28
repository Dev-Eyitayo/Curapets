from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Pet
from .serializers import PetSerializer

class PetListCreateView(generics.GenericAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_pets = Pet.objects.filter(owner=user)
        return user_pets

    def get(self, request,):
        pets = self.get_queryset()
        serializer = self.get_serializer(pets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(data=serializer.data, status=201)

class PetDetailView(generics.GenericAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)

    def get(self, request):
        pet = self.get_object()
        serializer = self.get_serializer(pet)
        return Response(serializer.data,status=200)

    def put(self, request):
        pet = self.get_object()
        serializer = self.get_serializer(pet, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request,):
        pet = self.get_object()
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
