# Generated by Django 5.1.2 on 2024-11-01 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='phone_number',
            new_name='phone',
        ),
    ]
