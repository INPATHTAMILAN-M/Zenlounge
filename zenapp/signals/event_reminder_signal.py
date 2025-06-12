from kombu.exceptions import OperationalError
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from zenapp.models import Event  # Make sure this import path matches your project structure
from datetime import datetime, timedelta, timezone

from zenapp.tasks import send_event_reminder

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Event)
def schedule_event_reminder(sender, instance, created, **kwargs):
    if created:
        reminder_time = datetime.combine(
            instance.start_date - timedelta(days=1),
            datetime.strptime("08:00", "%H:%M").time()
        )

        from django.utils.timezone import make_aware
        if timezone.is_naive(reminder_time):
            reminder_time = make_aware(reminder_time)

        try:
            send_event_reminder.apply_async((instance.id,), eta=reminder_time)
            print(f"[INFO] Scheduled reminder for event {instance.id} at {reminder_time}")
        except OperationalError as e:
            logger.warning(f"[ERROR] Could not schedule reminder for event {instance.id}: {e}")
            # Optionally: retry later or store in DB to retry in cron/job