# Generated by Django 4.1.7 on 2023-06-20 21:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postsale', '0013_alter_outbound_pay_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outbound',
            name='pay_date',
            field=models.DateField(default=datetime.date(2023, 6, 20)),
        ),
    ]