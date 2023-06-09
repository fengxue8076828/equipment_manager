# Generated by Django 4.1.7 on 2023-04-26 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info_manager', '0009_warehouse'),
        ('presale', '0006_rename_inbount_device_inbound'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Suppier',
            new_name='Supplier',
        ),
        migrations.RenameField(
            model_name='equipment',
            old_name='suppier',
            new_name='supplier',
        ),
        migrations.RemoveField(
            model_name='device',
            name='inbound_date',
        ),
        migrations.RemoveField(
            model_name='device',
            name='inbound_image',
        ),
        migrations.RemoveField(
            model_name='device',
            name='operator',
        ),
        migrations.AddField(
            model_name='device',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='presale.supplier'),
        ),
        migrations.AddField(
            model_name='inbound',
            name='amount',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='inbound',
            name='equipment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='presale.equipment'),
        ),
        migrations.AddField(
            model_name='inbound',
            name='warehouse',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='info_manager.warehouse'),
        ),
        migrations.AlterField(
            model_name='inbound',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='presale.supplier'),
        ),
    ]
