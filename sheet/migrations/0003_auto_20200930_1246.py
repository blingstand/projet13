# Generated by Django 3.1.1 on 2020-09-30 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sheet', '0002_auto_20200930_1055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='owner',
            old_name='name',
            new_name='owner_name',
        ),
        migrations.RenameField(
            model_name='owner',
            old_name='sex',
            new_name='owner_sex',
        ),
        migrations.RenameField(
            model_name='owner',
            old_name='surname',
            new_name='owner_surname',
        ),
    ]
