from django.contrib import admin
from .models import University, IntrestedTopic, CustomUser, PaymentGateway

admin.site.register(University)
admin.site.register(IntrestedTopic)
admin.site.register(CustomUser)
admin.site.register(PaymentGateway)
