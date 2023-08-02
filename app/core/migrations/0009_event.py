# Generated by Django 4.2.3 on 2023-07-20 05:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_equipment_number_alter_equipment_uid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('load_in_date', models.DateTimeField()),
                ('load_out_date', models.DateTimeField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('comment', models.TextField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.client')),
                ('crew', models.ManyToManyField(related_name='event_crew', to=settings.AUTH_USER_MODEL)),
                ('equipment', models.ManyToManyField(to='core.equipment')),
                ('leader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_leader', to=settings.AUTH_USER_MODEL)),
                ('venue', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.venue')),
            ],
        ),
    ]