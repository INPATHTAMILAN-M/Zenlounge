# Generated by Django 5.1.6 on 2025-03-03 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zenapp', '0015_payment_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='currency',
            field=models.CharField(default='INR', max_length=5),
        ),
    ]
