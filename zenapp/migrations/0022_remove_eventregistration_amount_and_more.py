# Generated by Django 5.1.6 on 2025-03-11 05:37

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zenapp', '0021_alter_eventregistration_registration_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventregistration',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='eventregistration',
            name='payment_status',
        ),
        migrations.AlterField(
            model_name='eventregistration',
            name='registration_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
