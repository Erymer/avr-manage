# Generated by Django 4.2.3 on 2023-07-19 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_equipment'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='equipment',
            name='uid',
            field=models.CharField(unique=True),
        ),
    ]
