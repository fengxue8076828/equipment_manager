# Generated by Django 4.1.7 on 2023-05-26 12:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("postsale", "0009_alter_outbound_pay_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="devicesold",
            name="state",
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name="outbound",
            name="pay_date",
            field=models.DateField(default=datetime.date(2023, 5, 26)),
        ),
    ]
