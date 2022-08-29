# Generated by Django 4.0.6 on 2022-08-13 10:31

from django.db import migrations, models
import django.db.models.deletion
import order.models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0021_requestrefundbankinfo_is_refunded'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestrefundbankinfo',
            name='price',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='requestrefundbankinfo',
            name='order_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='RequestRefundBankInfo', to='order.orderitem', validators=[order.models.validate_cod_refund]),
        ),
    ]