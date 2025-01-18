from django.shortcuts import render
from rest_framework import generics
from .serializers import RoomSerializer,OccupiedDateSerializer,UserSerializer
from .models import Room,OccupiedDate,User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed,PermissionDenied

# Create your views here.

@api_view(['GET'])
def api_root(request, format=None):
    print("The request is",request)
    return Response({
        
        'rooms': reverse('room-list', request=request, format=format),#generate the URL for a given view name
        
    })

class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    print("this is the queryset",queryset)
    serializer_class = RoomSerializer
    print("the serializer class is ",serializer_class)   

class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class OccupiedDatesList(generics.ListCreateAPIView):
    queryset = OccupiedDate.objects.all()
    serializer_class = OccupiedDateSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        user = self.request.user  
        if not user.is_superuser and not user.is_staff:
            return OccupiedDate.objects.filter(user=user)
        return super().get_queryset()
    
    
    

class OccupiedDatesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OccupiedDate.objects.all()
    serializer_class = OccupiedDateSerializer
    #permission_classes = [IsAdminOrReadOnly]    

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:  # Admin users
            return User.objects.all()
        else:  # Regular users
            return User.objects.filter(id=user.id)
    

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        user = self.request.user
        obj = super().get_object()

        # Allow access if the user is fetching their own details or is an admin
        if obj == user or user.is_staff or user.is_superuser:
            return obj
        else:
            pass#raise permissions.PermissionDenied("You do not have permission to access this user's details.")    
