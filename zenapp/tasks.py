import os
from dotenv import load_dotenv
from mailjet_rest import Client
from celery import shared_task
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from authapp.models import CustomUser
from zenapp.models import Event
from .models import EventRegistration
from django.conf import settings


load_dotenv()

MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")

@shared_task
def send_bulk_mailjet_emails(user_ids: list[int], event_id: int):
    mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY), version='v3.1')

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        print(f"Event with ID {event_id} does not exist.")
        return

    users = CustomUser.objects.filter(id__in=user_ids).order_by('id')
    paginator = Paginator(users, 50)

    for page_num in paginator.page_range:
        messages = []

        for user in paginator.page(page_num).object_list:
            html_content = render_to_string("event_reminder.html", {
                "user_name": user.email,
                "event_title": event.title,
                "event_start_date": event.start_date,
                "event_end_date": event.end_date,
                "event_start_time": event.start_time,
                "event_end_time": event.end_time,
                "event_location": "Online",
                "event_link": event.session_link,
            })

            messages.append({
                "From": {"Email": "zenlounge25@gmail.com", "Name": "ZenLounge"},
                "To": [{"Email": user.email, "Name": f"{user.first_name} {user.last_name}"}],
                "Subject": f"Event Update: {event.title}",
                "TextPart": "Event details are included below.",
                "HTMLPart": html_content,
            })

        if messages:
            try:
                response = mailjet.send.create(data={"Messages": messages})
                print(f"Batch {page_num}: {response.status_code}")
            except Exception as e:
                print(f"Error sending batch {page_num}: {str(e)}")




@shared_task
def send_event_reminder(event_id):
    try:
        event = Event.objects.get(id=event_id)
        registrations = EventRegistration.objects.filter(event=event)

        for registration in registrations:
            user = registration.user
            print(f"Sending reminder to {user.email} for event {event.title}")
            
            if user.email:
                html_message = render_to_string("event_reminder.html", {
                    "user": user,
                    "user_name": user.first_name or user.last_name,
                    "event": event
                })

                send_mail(
                    subject=f"Reminder: Upcoming Event - {event.title}",
                    message="This is a reminder for your upcoming event.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=True
                )
    except Event.DoesNotExist:
        pass