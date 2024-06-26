# Generated by Django 5.0.3 on 2024-05-07 17:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('boards', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseboard',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.region'),
        ),
        migrations.AddField(
            model_name='clubboard',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.club'),
        ),
        migrations.AddField(
            model_name='organizationboard',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.organization'),
        ),
    ]
