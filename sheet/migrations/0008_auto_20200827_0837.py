# Generated by Django 3.0.8 on 2020-08-27 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheet', '0007_auto_20200720_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='name',
            field=models.CharField(max_length=30, unique=True, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='owner',
            field=models.CharField(max_length=50, null=True, verbose_name='Idt du proprio'),
        ),
    ]
