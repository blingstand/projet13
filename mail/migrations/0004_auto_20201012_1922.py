# Generated by Django 3.1.1 on 2020-10-12 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0003_mail_send_after_delete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mail',
            name='send_at_this_date',
        ),
        migrations.RemoveField(
            model_name='mail',
            name='send_when_x_month',
        ),
        migrations.AddField(
            model_name='mail',
            name='send_every_2_weeks',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='mail',
            name='send_when_neuterable',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
