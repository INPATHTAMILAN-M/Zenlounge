# Generated by Django 5.1.6 on 2025-03-11 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zenapp', '0022_remove_eventregistration_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventregistration',
            name='registration_id',
            field=models.CharField(default='REGIS263837', max_length=10),
        ),
    ]
