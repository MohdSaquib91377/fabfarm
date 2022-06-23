# Generated by Django 4.0.5 on 2022-06-22 14:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('coupon', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=24)),
                ('city', models.CharField(max_length=24)),
                ('state', models.CharField(max_length=24)),
                ('country', models.CharField(max_length=24)),
                ('pincode', models.IntegerField()),
                ('locality', models.CharField(max_length=64)),
                ('landmark', models.CharField(max_length=64, null=True)),
                ('address', models.TextField()),
                ('alternate_number', models.IntegerField()),
                ('total_price', models.FloatField(null=True)),
                ('payment_mode', models.CharField(max_length=64, null=True)),
                ('payment_id', models.CharField(max_length=64, null=True)),
                ('message', models.TextField(null=True)),
                ('tracking_no', models.CharField(max_length=64, null=True)),
                ('order_status', models.CharField(choices=[('order_cancelled', 'order cancelled'), ('order_pending', 'order pending'), ('order_success', 'order success')], default='order_pending', max_length=16)),
                ('discounted_price', models.FloatField(default=0)),
                ('total_amount_payble', models.FloatField(default=0)),
                ('razorpay_order_id', models.CharField(blank=True, max_length=64, null=True)),
                ('razorpay_status', models.CharField(blank=True, max_length=16, null=True)),
                ('amount_due', models.PositiveBigIntegerField(blank=True, default=0, null=True)),
                ('amount_paid', models.PositiveBigIntegerField(blank=True, default=0, null=True)),
                ('attempts', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('payment_status', models.CharField(choices=[('payment_failed', 'payment failed'), ('payment_success', 'payment success'), ('payment_pending', 'payment pending')], default='payment_pending', max_length=16)),
                ('coupon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='coupon.coupon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('price', models.FloatField(null=True)),
                ('quantity', models.IntegerField(null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Out For Shipping', 'Out For Shiping'), ('Completed', 'Completed'), ('Packed', 'Packed'), ('Cancel', 'Cancel')], default='Pendding', max_length=64)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderItem', to='order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderItem', to='store.product')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
