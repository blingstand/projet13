# Generated by Django 3.0.8 on 2020-09-28 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheet', '0027_auto_20200926_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='nature',
            field=models.CharField(default='à compléter', max_length=1),
        ),
    ]
