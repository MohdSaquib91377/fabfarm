# Generated by Django 4.0.6 on 2022-08-17 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0022_requestrefundbankinfo_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestrefundbankinfo',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='RequestRefundBankInfo', to='order.order'),
        ),
    ]
