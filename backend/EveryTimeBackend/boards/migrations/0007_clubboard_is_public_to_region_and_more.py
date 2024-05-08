# Generated by Django 5.0.3 on 2024-05-08 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0006_baseboard_is_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubboard',
            name='is_public_to_region',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='organizationboard',
            name='is_public_to_region',
            field=models.BooleanField(default=False),
        ),
    ]
