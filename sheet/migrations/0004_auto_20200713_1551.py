# Generated by Django 3.0.8 on 2020-07-13 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheet', '0003_auto_20200713_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='owner',
            field=models.CharField(max_length=50, null=True, unique=True, verbose_name='Idt du proprio'),
        ),
    ]
