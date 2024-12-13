# Generated by Django 5.1.2 on 2024-11-25 15:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0017_rename_user_ticket_created_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=100)),
                ('venue', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('description', models.TextField(blank=True, null=True)),
                ('send_email', models.BooleanField(default=False)),
                ('important', models.BooleanField(default=False)),
                ('event_image', models.FileField(blank=True, null=True, upload_to='attachments/')),
                ('individual_users', models.ManyToManyField(blank=True, null=True, related_name='invited_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]