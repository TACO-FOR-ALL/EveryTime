# Generated by Django 5.0.3 on 2024-05-15 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_delete_postmedia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpostprofile',
            name='posts',
            field=models.ManyToManyField(blank=True, to='posts.post'),
        ),
    ]
