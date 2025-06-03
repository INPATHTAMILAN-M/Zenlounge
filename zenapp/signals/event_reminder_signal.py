from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime, timedelta

from zenapp.models import Event
from zenapp.tasks import send_event_reminder

@receiver(post_save, sender=Event)
def schedule_event_reminder(sender, instance, created, **kwargs):
    if created:
        # Schedule task 1 day before event start date at 8 AM
        reminder_time = datetime.combine(
            instance.start_date - timedelta(days=1),
            datetime.strptime("08:00", "%H:%M").time()
        )

        print(f"Scheduling reminder for event {instance.id} at {reminder_time}")

        # Ensure it's timezone-aware
        from django.utils.timezone import make_aware
        if timezone.is_naive(reminder_time):
            reminder_time = make_aware(reminder_time)

        # Schedule task
        send_event_reminder.apply_async((instance.id,), eta=reminder_time)