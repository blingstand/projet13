# Generated by Django 3.0.8 on 2020-08-27 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheet', '0008_auto_20200827_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Nom'),
        ),
    ]
