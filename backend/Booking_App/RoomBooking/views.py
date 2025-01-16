from django.shortcuts import render
from rest_framework import generics
from .serializers import RoomSerializer
from .models import Room
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

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
 