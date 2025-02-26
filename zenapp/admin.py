from django.contrib import admin
from .models import Category, Event, EventRegistration, EventLog

admin.site.site_header = 'ZenLounge Admin'
admin.site.site_title = 'ZenLounge Admin Portal'
admin.site.index_title = 'Welcome to ZenLounge Admin Portal'


admin.site.register(Category)
admin.site.register(Event)
admin.site.register(EventRegistration)
admin.site.register(EventLog)

