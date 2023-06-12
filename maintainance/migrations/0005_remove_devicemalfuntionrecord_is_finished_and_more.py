# Generated by Django 4.1.7 on 2023-06-02 11:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("maintainance", "0004_devicemalfuntionrecord_is_finished"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="devicemalfuntionrecord",
            name="is_finished",
        ),
        migrations.AddField(
            model_name="devicemalfuntionrecord",
            name="maintainer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="maintainer",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="devicemalfuntionrecord",
            name="state",
            field=models.CharField(default="assigned", max_length=50),
        ),
        migrations.AlterField(
            model_name="devicemalfuntionrecord",
            name="operator",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="operator",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
