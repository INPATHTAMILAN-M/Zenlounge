# Generated by Django 5.1.6 on 2025-03-03 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zenapp', '0014_alter_payment_payment_gateway'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='currency',
            field=models.CharField(default='INR', max_length=3),
        ),
    ]
