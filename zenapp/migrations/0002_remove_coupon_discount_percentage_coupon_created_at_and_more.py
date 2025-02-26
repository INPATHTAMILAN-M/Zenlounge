# Generated by Django 5.1.6 on 2025-02-26 09:17

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zenapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='discount_percentage',
        ),
        migrations.AddField(
            model_name='coupon',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coupon',
            name='discount_type',
            field=models.CharField(choices=[('percentage', 'Percentage'), ('fixed', 'Fixed Amount')], default='percentage', max_length=10),
        ),
        migrations.AddField(
            model_name='coupon',
            name='discount_value',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, verbose_name='Discount Value'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coupon',
            name='max_discount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Maximum Discount Allowed'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='min_order_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Minimum Order Value'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='coupon',
            name='usage_limit',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Total Usage Limit'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='used_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Used Count'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(max_length=20, unique=True, verbose_name='Coupon Code'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='valid_from',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='valid_to',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
