# Generated by Django 3.1.1 on 2020-10-04 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheet', '0003_auto_20200930_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='caution',
            field=models.CharField(max_length=5, verbose_name='Montant de la caution(sans €)'),
        ),
    ]
