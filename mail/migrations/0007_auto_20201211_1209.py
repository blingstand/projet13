# Generated by Django 3.1.1 on 2020-12-11 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0006_auto_20201210_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='condition',
            field=models.IntegerField(blank=True, choices=[(1, 'creation animal stéril'), (2, 'creation animal non stéril'), (3, 'modif caution'), (4, 'suppression animal'), (5, 'envoie toute les 2 semaines'), (6, 'animal devient stéril')], null=True),
        ),
    ]
