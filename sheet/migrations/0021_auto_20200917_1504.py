# Generated by Django 3.0.8 on 2020-09-17 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheet', '0020_auto_20200917_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='mail_reminder',
            field=models.CharField(default=0, max_length=3, verbose_name='Nombre de mail envoyés'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='tel_reminder',
            field=models.CharField(default=0, max_length=3, verbose_name="Nombre d'appel passés"),
        ),
    ]