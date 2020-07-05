# Generated by Django 3.0.8 on 2020-07-03 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sheet', '0003_auto_20200703_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='admin_data_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sheet.AdminData', verbose_name='Suivi administratif'),
        ),
        migrations.AlterField(
            model_name='animal',
            name='color',
            field=models.CharField(max_length=30, verbose_name='Couleur'),
        ),
        migrations.AlterField(
            model_name='animal',
            name='is_cat',
            field=models.BooleanField(default=True, verbose_name="espèce : Cocher si c'est un chat"),
        ),
        migrations.AlterField(
            model_name='animal',
            name='is_male',
            field=models.BooleanField(default=True, verbose_name="espèce : Cocher si c'est un mâle"),
        ),
        migrations.AlterField(
            model_name='animal',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='animal',
            name='owner_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sheet.Owner', verbose_name='Propriétaire'),
        ),
    ]