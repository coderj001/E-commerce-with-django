# Generated by Django 3.0 on 2020-09-07 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200907_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='discount_price',
            field=models.FloatField(blank=True, null=True, verbose_name='Item discount price'),
        ),
    ]
