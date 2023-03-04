from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from djangoopencv.serializers import UserSerializer, GroupSerializer
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework.request import Request
import requests
import cv2
import numpy as np
from django.http import JsonResponse

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET', 'POST'])
def DetectImage(request):
    try:
        allUser = User.objects.all().order_by('-date_joined')
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserSerializer(allUser, many=True, context={ "request": request })
        return Response(serializer.data)
    elif request.method == "POST":
        print(request.data.get('url'))
        url = request.data.get('url')
        # Download image from URL
        img_response = requests.get(url)
        img_array = np.array(bytearray(img_response.content), dtype=np.uint8)
        img = cv2.imdecode(img_array, -1)

        # Load the pre-trained human detection model
        human_cascade = cv2.CascadeClassifier('./haarcascade.xml')

        # Detect humans in the image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        humans = human_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

        # Return the coordinates of the detected humans
        results = [{'x': x, 'y': y, 'width': w, 'height': h} for (x, y, w, h) in humans]

        return JsonResponse({ "results": results })
    return Response(serializer.data)



class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]