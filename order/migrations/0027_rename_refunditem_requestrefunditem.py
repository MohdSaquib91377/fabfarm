# Generated by Django 4.0.6 on 2022-08-29 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_remove_fundaccout_make_refund'),
        ('order', '0026_refunditem'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RefundItem',
            new_name='RequestRefundItem',
        ),
    ]