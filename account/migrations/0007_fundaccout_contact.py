# Generated by Django 4.0.6 on 2022-08-26 10:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_useraddress_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundAccout',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contact_id', models.CharField(max_length=64, verbose_name='contact id')),
                ('razorpay_fund_id', models.CharField(max_length=64, verbose_name='razorpay fund id')),
                ('account_type', models.CharField(max_length=64)),
                ('ifsc', models.CharField(max_length=64)),
                ('bank_name', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('account_number', models.PositiveIntegerField()),
                ('active', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fund_acc', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Fund Account',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('razorpay_conatct_id', models.CharField(max_length=64, verbose_name='razorpay contact id')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Razorpay Contact',
                'db_table': 'contacts',
                'ordering': ['-id'],
            },
        ),
    ]
