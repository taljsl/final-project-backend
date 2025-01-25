from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password

# Handles user registration.
@api_view(['POST'])
def register_user(request):    
    data = request.data
    try:
        # Check if username or email is already taken
        if CustomUser.objects.filter(username=data['username']).exists():
            return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)
        #Check if email is in use
        if CustomUser.objects.filter(email=data['email']).exists():
            return Response({'error': 'Email already in use'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = CustomUser.objects.create(
            username=data['username'],
            email=data['email'],
            name=data.get('name', ''),  
            nickname=data.get('nickname', ''),  
            #the function here hash's the password
            password=make_password(data['password'])  
        )

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    #Return an error if missing a required field
    except KeyError as e:
        return Response({'error': f'Missing field: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
#Only authenticated users can access this
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status= status.HTTP_200_OK)



@api_view('GET','PUT')
@permission_classes(IsAuthenticated)
def updateUser(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.methos == 'PUT':
        # partial=True allows updating specific fields
        serializer = UserSerializer(user, data=request.data, partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
