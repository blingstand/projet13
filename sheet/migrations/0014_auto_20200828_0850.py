# Generated by Django 3.0.8 on 2020-08-28 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sheet', '0013_auto_20200828_0846'),
    ]

    operations = [
        migrations.RenameField(
            model_name='owner',
            old_name='owner_sexe',
            new_name='owner_sex',
        ),
    ]
