from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    PasswordResetSerializer, PasswordConfirmSerializer, UserSignupSerializer,ChangePasswordSerializer
)
from .utils.email_sender import send_email

User = get_user_model()


class UserRegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSignupSerializer
    
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User Created Successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSignupSerializer
    
    def get_object(self):
        return self.request.user

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        # Check if email exists in the database
        user = User.objects.filter(email=email).first()
        if user and not user.check_password(password):
            return Response({"detail": "Incorrect password."}, status=status.HTTP_401_UNAUTHORIZED)
        elif not user:
            return Response({"detail": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        token_response = super().post(request, *args, **kwargs)
        token_response.data['user_id'] = user.id
        token_response.data['email'] = user.email
        token_response.data['username'] = user.first_name + " " + user.last_name
        token_response.data['group'] = user.groups.values_list('name', flat=True)
        return token_response
    

class ChangePasswordViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def create(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data["new_password"])
            user.save()

            # Keep the user logged in
            update_session_auth_hash(request, user)

            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
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
            reset_url = f"{settings.FRONTEND_URL}/forgot-new-password/?id={user.pk}&token={token}/"

            # Send email
            send_email(
                subject="Reset Your Password",
                to_email=user.email,
                template_name='password_reset.html',
                context={"url": reset_url},
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
            login_url = f"{settings.FRONTEND_URL}/login/"
            send_email(
                subject="Password Reset Successful",
                to_email=user.email,
                template_name='password_reset_confirm.html',
                context={"login_url": login_url},
            )

            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
