# Generated by Django 5.1.2 on 2024-11-17 14:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0012_categories'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apis.categories')),
            ],
        ),
    ]
