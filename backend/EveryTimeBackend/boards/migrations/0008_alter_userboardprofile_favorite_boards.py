# Generated by Django 5.0.3 on 2024-05-15 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0007_clubboard_is_public_to_region_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userboardprofile',
            name='favorite_boards',
            field=models.ManyToManyField(blank=True, related_name='favorited_by', to='boards.baseboard'),
        ),
    ]
