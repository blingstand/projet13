# Generated by Django 3.1.1 on 2020-09-29 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('mail_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50, unique=True)),
                ('resume', models.CharField(blank=True, max_length=120)),
                ('full_text', models.TextField(blank=True)),
                ('auto_send', models.BooleanField(blank=True, default=False)),
                ('send_after_creation', models.BooleanField(blank=True, default=False)),
                ('send_after_modif', models.BooleanField(blank=True, default=False)),
                ('send_when_x_month', models.IntegerField(blank=True, default=None, null=True)),
                ('send_at_this_date', models.DateField(blank=True, default=None, null=True)),
            ],
        ),
    ]
