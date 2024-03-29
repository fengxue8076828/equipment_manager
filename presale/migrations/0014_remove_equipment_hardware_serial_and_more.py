# Generated by Django 4.1.7 on 2023-09-11 14:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("presale", "0013_supplier_is_active"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="equipment",
            name="hardware_serial",
        ),
        migrations.RemoveField(
            model_name="equipment",
            name="software_serial",
        ),
        migrations.AddField(
            model_name="device",
            name="hardware_serial",
            field=models.CharField(default=1234567, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="device",
            name="software_serial",
            field=models.CharField(default=1234567, max_length=200),
            preserve_default=False,
        ),
    ]
