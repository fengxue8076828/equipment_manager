# Generated by Django 4.1.7 on 2023-04-26 11:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postsale', '0004_remove_devicesold_buyer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outbound',
            name='pay_date',
            field=models.DateField(default=datetime.date(2023, 4, 26)),
        ),
    ]
