from django.urls import path, include
from rest_framework import routers
from . import viewsets

router = routers.DefaultRouter()
router.register(r'categories', viewsets.CategoryViewSet)
router.register(r'events', viewsets.EventViewSet)
router.register(r'event-registrations', viewsets.EventRegistrationViewSet)
router.register(r'event-logs', viewsets.EventLogViewSet)
router.register(r'zoom-meeting-attendances', viewsets.ZoomMeetingAttendanceViewSet)
router.register(r'payments', viewsets.PaymentViewSet)
router.register(r'coupons', viewsets.CouponViewSet)
router.register(r'customer-supports', viewsets.CustomerSupportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
