# Generated by Django 4.0.6 on 2022-08-02 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_refund'),
    ]

    operations = [
        migrations.AddField(
            model_name='refund',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]