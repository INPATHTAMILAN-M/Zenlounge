from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
# from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from .serializers import PasswordResetSerializer, PasswordConfirmSerializer, UserSignupSerializer
from .utils.email_sender import send_email

User = get_user_model()


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

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = get_object_or_404(User, email=email)

            # Generate password reset token
            token = default_token_generator.make_token(user)
            print(token)
            print(user.pk)
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{user.pk}/{token}/"

            # Send email
            send_email(
                "Reset Your Password",
                settings.DEFAULT_FROM_EMAIL,
                'password_reset.html',
                {"url": reset_url},
            )

            return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    """
    API for confirming and setting a new password.
    """
    permission_classes = [AllowAny]
    serializer_class = PasswordConfirmSerializer


    def post(self, request, uidb64, token):
        serializer = PasswordConfirmSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, pk=uidb64)

            # Verify token
            if not default_token_generator.check_token(user, token):
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

            # Set new password
            user.set_password(serializer.validated_data["new_password"])
            user.save()

            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
