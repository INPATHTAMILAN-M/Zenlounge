# Generated by Django 5.1.6 on 2025-03-11 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zenapp', '0024_alter_eventregistration_registration_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventregistration',
            name='registration_id',
            field=models.CharField(blank=True, default='REGIS644574', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='eventregistration',
            name='registration_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Completed', max_length=20),
        ),
    ]
