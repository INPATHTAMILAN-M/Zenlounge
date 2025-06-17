from django.dispatch import receiver
from django.db.models.signals import post_save  
from zenapp.models import Event, EventRegistration 
from authapp.utils.email_sender import send_email  
from authapp.models import CustomUser
from zenapp.tasks import send_event_creation_emails_task

@receiver(post_save, sender=Event)
def send_event_creation_email(sender, instance:Event, created, **kwargs):
    print("Event creation signal received")
    if not created:
        return
    send_event_creation_emails_task.apply_async((instance.id,))


@receiver(post_save, sender=Event)
def send_event_update_email(sender, instance:Event, created, **kwargs):
    
    if created:  
        return

    registered_users = EventRegistration.objects.filter(event=instance).select_related("user")

    if not registered_users.exists():
        return

    for registration in registered_users:
        user = registration.user

        # Render the email template with dynamic content
        content = {
            "user_name": user.first_name + " " + user.last_name,
            "event_title": instance.title,
            "event_start_date": instance.start_date,
            "event_end_date": instance.end_date,
            "event_start_time": instance.start_time,
            "event_end_time": instance.end_time,
            "event_category": instance.lounge_type.name,
            "registration_id": registration.registration_id,
            "registration_status": registration.registration_status,
            "event_location": "Online",
            "event_link": instance.session_link
            
        }
        template = "event_update_notify.html"
        send_email("Event Update", user.email, template, content)
        
        
        