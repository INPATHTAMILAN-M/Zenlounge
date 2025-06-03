from django.apps import AppConfig


class ZenappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'zenapp'

    def ready(self):
        # import zenapp.signals.event_update_signal
        import zenapp.signals.event_reminder_signal
