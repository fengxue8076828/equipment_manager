# Generated by Django 4.1.7 on 2023-06-13 11:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("presale", "0012_equipment_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="supplier",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
