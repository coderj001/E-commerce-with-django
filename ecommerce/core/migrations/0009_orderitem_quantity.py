# Generated by Django 3.0 on 2020-09-07 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_item_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
