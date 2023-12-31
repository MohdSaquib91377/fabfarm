# Generated by Django 4.0.6 on 2022-07-18 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=64, null=True)),
                ('razorpay_order_id', models.CharField(blank=True, max_length=64, null=True)),
                ('razorpay_signature', models.CharField(blank=True, max_length=64, null=True)),
                ('method', models.CharField(blank=True, max_length=64, null=True)),
                ('fee', models.CharField(blank=True, max_length=64, null=True)),
                ('tax', models.CharField(blank=True, max_length=64, null=True)),
                ('error_code', models.TextField(blank=True, null=True)),
                ('error_description', models.TextField(blank=True, null=True)),
                ('error_source', models.TextField(blank=True, null=True)),
                ('error_step', models.TextField(blank=True, null=True)),
                ('error_reason', models.CharField(blank=True, max_length=64, null=True)),
                ('error_order_id', models.TextField(blank=True, null=True)),
                ('error_payment_id', models.TextField(blank=True, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='order.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Payments',
            },
        ),
    ]
