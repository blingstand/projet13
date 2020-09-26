# Generated by Django 3.0.8 on 2020-09-09 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheet', '0017_auto_20200907_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admindata',
            name='is_neutered',
            field=models.SmallIntegerField(default=0, verbose_name='statut stérilisation (stérile, stérilisable, à stériliser)'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='owner_sex',
            field=models.SmallIntegerField(default=0, null=True, verbose_name='Sexe propriétaire\n (0 = H / 1 = F)'),
        ),
    ]