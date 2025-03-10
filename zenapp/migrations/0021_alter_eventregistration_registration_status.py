# Generated by Django 5.1.6 on 2025-03-08 04:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("zenapp", "0020_alter_eventregistration_registration_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventregistration",
            name="registration_status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Completed", "Completed"),
                    ("Failed", "Failed"),
                ],
                default="Pending",
                max_length=20,
            ),
        ),
    ]
