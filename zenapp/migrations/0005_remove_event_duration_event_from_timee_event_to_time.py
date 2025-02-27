# Corrected migration file

from django.db import migrations, models
import datetime  # Import datetime to use a proper time value

class Migration(migrations.Migration):

    dependencies = [
        ('zenapp', '0004_event_lounge_type_event_seat_count_delete_seat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='duration',
        ),
        migrations.AddField(
            model_name='event',
            name='from_timee',
            field=models.TimeField(default=datetime.time(0, 0, 0)),  # Default to midnight
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='to_time',
            field=models.TimeField(default=datetime.time(0, 0, 0)),  # Default to midnight
            preserve_default=False,
        ),
    ]
