from django.dispatch import receiver
from django.db.models.signals import post_save  
from zenapp.models import Event, EventRegistration 
from authapp.utils.email_sender import send_email  



@receiver(post_save, sender=Event)
def send_event_update_email(sender, instance, created, **kwargs):
    
    if created:  # Ignore if event is newly created
        return

    registered_users = EventRegistration.objects.filter(event=instance).select_related("user")

    if not registered_users.exists():
        return

    for registration in registered_users:
        user = registration.user

        # Render the email template with dynamic content
        content = {
            "user_name": user.email,
            "event_title": instance.title,
            "event_start_date": instance.start_date,
            "event_end_date": instance.end_date,
            "event_start_time": instance.start_time,
            "event_end_time": instance.end_time,
            "event_location": "Online",
            "event_link": instance.session_link
            
        }
        template = "event_update_notify.html"
        send_email("Event Update", user.email, template, content)
        
        
        