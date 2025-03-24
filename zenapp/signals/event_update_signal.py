from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.dispatch import receiver
from django.db.models.signals import post_save  # Import post_save signal
from zenapp.models import Event, EventRegistration  # Import the Event and EventRegistration models


@receiver(post_save, sender=Event)
def send_event_update_email(sender, instance, created, **kwargs):
    """Send email notifications when an event is updated."""
    if created:  # Ignore if event is newly created
        return

    registered_users = EventRegistration.objects.filter(event=instance).select_related("user")

    if not registered_users.exists():
        return

    for registration in registered_users:
        user = registration.user

        # Render the email template with dynamic content
        html_content = render_to_string("emails/event_update.html", {
            "user_name": user.get_full_name(),
            "event_title": instance.title,
            "event_start_date": instance.start_date,
            "event_end_date": instance.end_date,
            "event_start_time": instance.start_time,
            "event_end_time": instance.end_time,
            "event_location": "Online" if not instance.session_link else instance.session_link,
            "event_link": f"https://yourdomain.com/events/{instance.id}/"
        })
        
        text_content = strip_tags(html_content)  # Convert HTML to plain text

        email = EmailMultiAlternatives(
            subject=f"Update: Event '{instance.title}' has been modified",
            body=text_content,
            from_email="no-reply@yourdomain.com",
            to=[user.email]
        )
        email.attach_alternative(html_content, "text/html")  # Attach HTML version
        email.send(fail_silently=True)