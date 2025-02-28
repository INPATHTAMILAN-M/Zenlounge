# Generated by Django 5.1.6 on 2025-02-27 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0005_alter_customuser_managers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentGateway',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('secret_key', models.CharField(max_length=255)),
                ('public_key', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
