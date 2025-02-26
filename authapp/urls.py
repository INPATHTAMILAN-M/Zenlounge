from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView, 
    TokenBlacklistView,
)
from .views import (
    UserRegistrationAPIView,
    UserProfileAPIView,
    PasswordResetAPIView,
    PasswordResetConfirmAPIView,
    
)
from .viewset import UniversityViewSet,IntrestedTopicViewSet, CustomUserViewSet

router = DefaultRouter()

router.register(r'universities', UniversityViewSet)
router.register(r'interested-topics', IntrestedTopicViewSet)
router.register(r'users', CustomUserViewSet)



urlpatterns = [
    path('signup/', UserRegistrationAPIView.as_view(), name='signup_user'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('password-reset/', PasswordResetAPIView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),
    path('', include(router.urls)),
]