# Generated by Django 3.0.8 on 2020-08-31 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheet', '0014_auto_20200828_0850'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='observation',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]