# Generated by Django 4.1.1 on 2022-09-17 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airportmgt', '0003_alter_appuser_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='suspension_expires',
            field=models.DateField(blank=True, null=True, verbose_name='suspensions_expires'),
        ),
    ]
