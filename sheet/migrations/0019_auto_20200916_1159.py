# Generated by Django 3.0.8 on 2020-09-16 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheet', '0018_auto_20200909_1523'),
    ]

    operations = [
        migrations.RenameField(
            model_name='owner',
            old_name='contact_id',
            new_name='contact',
        ),
        migrations.AddField(
            model_name='owner',
            name='need_contact',
            field=models.BooleanField(default=True),
        ),
    ]