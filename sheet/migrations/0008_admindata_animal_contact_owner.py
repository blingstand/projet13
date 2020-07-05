# Generated by Django 3.0.8 on 2020-07-03 09:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sheet', '0007_auto_20200703_0907'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminData',
            fields=[
                ('admin_data_id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.IntegerField(blank=True, default=0, unique=True, verbose_name='Numéro de dossier')),
                ('chip', models.IntegerField(blank=True, default=0, unique=True, verbose_name='Numéro de puce')),
                ('tatoo', models.IntegerField(blank=True, default=0, unique=True, verbose_name='Numéro de tatouage')),
                ('is_neutered', models.BooleanField(default=False, verbose_name='Stérilisé')),
                ('can_be_neutered', models.BooleanField(default=False, verbose_name='Doit être stérilisé')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('contact_id', models.AutoField(primary_key=True, serialize=False)),
                ('contact_date', models.DateField(default=django.utils.timezone.now, verbose_name='Date du contact')),
                ('resume', models.CharField(blank=True, max_length=90)),
                ('full_text', models.TextField(blank=True)),
                ('is_mail', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('owner_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, verbose_name='Nom')),
                ('surname', models.CharField(max_length=30, verbose_name='Prénom')),
                ('telephone', models.IntegerField(unique=True, verbose_name='Téléphone')),
                ('mail', models.EmailField(max_length=254, unique=True, verbose_name='Mail')),
                ('nb_mail_send', models.SmallIntegerField(default=0, verbose_name='Nombre de mail envoyés')),
                ('nb_call', models.SmallIntegerField(default=0, verbose_name="Nombre d'appel passés")),
                ('contact_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sheet.Contact', verbose_name='Gestion des contacts')),
            ],
        ),
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('animal_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, verbose_name='Nom')),
                ('date_of_birth', models.DateField(verbose_name='Date de naissance')),
                ('race', models.CharField(max_length=50)),
                ('is_cat', models.BooleanField(default=True, verbose_name="Espèce : Cocher si c'est un chat")),
                ('color', models.CharField(max_length=30, verbose_name='Couleur')),
                ('is_male', models.BooleanField(default=True, verbose_name="Sexe : Cocher si c'est un mâle")),
                ('date_of_adoption', models.DateField(default=django.utils.timezone.now, verbose_name="Date d'adoption")),
                ('admin_data_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sheet.AdminData', verbose_name='Suivi administratif')),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sheet.Owner', verbose_name='Propriétaire')),
            ],
        ),
    ]