# Generated by Django 5.1.2 on 2024-11-04 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0008_rename_building_id_floor_building'),
    ]

    operations = [
        migrations.RenameField(
            model_name='floor',
            old_name='building',
            new_name='building_id',
        ),
    ]