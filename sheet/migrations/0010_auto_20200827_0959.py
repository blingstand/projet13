# Generated by Django 3.0.8 on 2020-08-27 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheet', '0009_auto_20200827_0906'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='owner',
            name='owner',
        ),
        migrations.AddField(
            model_name='owner',
            name='owner_name',
            field=models.CharField(max_length=50, null=True, verbose_name='Prénom propriétaire'),
        ),
        migrations.AddField(
            model_name='owner',
            name='owner_sexe',
            field=models.CharField(max_length=1, null=True, verbose_name='Sexe propriétaire (H/F)'),
        ),
        migrations.AddField(
            model_name='owner',
            name='owner_surnname',
            field=models.CharField(max_length=50, null=True, verbose_name='Nom propriétaire'),
        ),
    ]