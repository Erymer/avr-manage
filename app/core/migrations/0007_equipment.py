# Generated by Django 4.2.3 on 2023-07-18 23:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_equipmenttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField()),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.equipmentbrand')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.equipmentmodel')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.equipmenttype')),
            ],
        ),
    ]
