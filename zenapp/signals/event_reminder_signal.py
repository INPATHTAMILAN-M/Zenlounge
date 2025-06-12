from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime, timedelta
from kombu.exceptions import OperationalError
import logging

from zenapp.models import Event
from zenapp.tasks import send_event_reminder

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Event)
def schedule_event_reminder(sender, instance, created, **kwargs):
    if created:
        try:
            # Schedule the reminder for 1 day before the event at 8:00 AM
            reminder_time = datetime.combine(
                instance.start_date - timedelta(days=1),
                datetime.strptime("08:00", "%H:%M").time()
            )

            # Make reminder_time timezone-aware
            if timezone.is_naive(reminder_time):
                reminder_time = timezone.make_aware(reminder_time)

            # Send task to Celery
            send_event_reminder.apply_async((instance.id,), eta=reminder_time)
            logger.info(f"Scheduled reminder for event {instance.id} at {reminder_time}")

        except OperationalError as e:
            logger.warning(f"Could not schedule reminder for event {instance.id}: {e}")
