# Generated by Django 5.0.5 on 2024-05-07 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='year',
            new_name='release_year',
        ),
    ]