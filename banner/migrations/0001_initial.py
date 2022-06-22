# Generated by Django 4.0.5 on 2022-06-21 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image_or_video', models.FileField(upload_to='banner')),
                ('caption', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('page', models.CharField(choices=[('Home', 'Home'), ('About', 'About'), ('Contact', 'Contact'), ('Filter', 'Filter')], default='Home', max_length=64)),
            ],
            options={
                'db_table': 'banners',
            },
        ),
    ]
