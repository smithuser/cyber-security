# Generated by Django 4.1.1 on 2022-09-18 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('airportmgt', '0007_remove_bannedmac_attack_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bannedmac',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='bannedmac',
            name='modified_at',
        ),
    ]