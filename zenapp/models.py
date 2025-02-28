from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid

# Lounge Categories
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    lounge_type = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.TimeField()
    end_time = models.TimeField()
    session_link = models.URLField(blank=True, null=True,max_length=500)
    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)    
    seat_count = models.IntegerField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# Event Registration
class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='event_registrations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default='Pending')
    registration_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.amount:
            self.amount = self.event.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Registration for {self.event.title} by {self.user.email}"    


# Event Logs
class EventLog(models.Model):
    category = models.CharField(max_length=255)
    event_name = models.CharField(max_length=255)
    meeting_id = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=255)
    user_email = models.EmailField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    participants = models.IntegerField()

    def __str__(self):
        return f"Event Log {self.meeting_id} - {self.username}"


# Zoom Meeting Attendance
class ZoomMeetingAttendance(models.Model):
    program_name = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    meeting_id = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=255)
    user_email = models.EmailField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    participants = models.IntegerField()

    def __str__(self):
        return f"Meeting {self.meeting_id} - {self.username}"

# Payments
class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registration = models.ForeignKey(EventRegistration, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])

    def __str__(self):
        return f"Payment {self.id} - {self.user.email}"

# Coupons & Discounts
class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]

    code = models.CharField(max_length=20, unique=True, verbose_name=_("Coupon Code"))
    discount_type = models.CharField(
        max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percentage'
    )
    discount_value = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Discount Value")
    )
    min_order_value = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Minimum Order Value")
    )
    max_discount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Maximum Discount Allowed")
    )
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField(null=True, blank=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Total Usage Limit"))
    used_count = models.PositiveIntegerField(default=0, verbose_name=_("Used Count"))
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Customer Support
class CustomerSupport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Support Ticket {self.id} - {self.user.username}"
