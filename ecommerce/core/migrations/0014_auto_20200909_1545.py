# Generated by Django 3.0 on 2020-09-09 15:45

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20200909_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='countries',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]