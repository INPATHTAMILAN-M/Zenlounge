from kombu.exceptions import OperationalError
import logging

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