# Generated by Django 4.2.3 on 2023-08-02 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_venue_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venue',
            name='user',
        ),
    ]
