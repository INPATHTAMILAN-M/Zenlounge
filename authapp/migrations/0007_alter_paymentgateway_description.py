# Generated by Django 5.1.6 on 2025-03-03 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_paymentgateway'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentgateway',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
