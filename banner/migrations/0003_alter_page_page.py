# Generated by Django 4.0.6 on 2022-07-26 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0002_alter_page_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='page',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]