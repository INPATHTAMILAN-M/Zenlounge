from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView, 
    TokenBlacklistView,
)
from .views import (
    CustomTokenObtainPairView,
    UserRegistrationAPIView,
    UserProfileAPIView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    ChangePasswordViewSet
    
)
from .viewset import (
    UniversityViewSet,IntrestedTopicViewSet, 
    CustomUserViewSet,PaymentGatewayViewSet,GroupViewSet,
    CountryViewSet
)
router = DefaultRouter()

router.register(r'universities', UniversityViewSet)
router.register(r'interested-topics', IntrestedTopicViewSet)
router.register(r'users', CustomUserViewSet)
router.register(r'payment-gateways', PaymentGatewayViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'change-password', ChangePasswordViewSet, basename='change-password')



urlpatterns = [
    path('', include(router.urls)),
    path('signup/', UserRegistrationAPIView.as_view(), name='signup_user'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
]
