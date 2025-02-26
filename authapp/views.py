from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import login
from .utils.email_sender import send_email
from .serializers import UserSignupSerializer, PasswordResetSerializer
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class UserRegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSignupSerializer
    
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSignupSerializer
    
    def get_object(self):
        return self.request.user

class PasswordResetAPIView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password reset email has been sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmAPIView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, uidb64, token):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                validate_email(serializer.data['email'])
                serializer.save(uidb64=uidb64, token=token)
                send_email("Password Reset", "Your password has been reset successfully.", [serializer.data['email']])
                return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
            except ValidationError:
                return Response({"detail": "Invalid email address."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
