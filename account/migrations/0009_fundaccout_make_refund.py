# Generated by Django 4.0.6 on 2022-08-29 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_fundaccout_account_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundaccout',
            name='make_refund',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='make refund for cash on delivery'),
        ),
    ]