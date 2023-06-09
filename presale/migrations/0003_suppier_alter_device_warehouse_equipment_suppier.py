# Generated by Django 4.1.7 on 2023-04-13 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info_manager', '0009_warehouse'),
        ('presale', '0002_alter_device_inbound_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suppier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('telephone', models.CharField(max_length=200)),
                ('email', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.CharField(max_length=300)),
                ('memo', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AlterField(
            model_name='device',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='devices', to='info_manager.warehouse'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='suppier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='presale.suppier'),
        ),
    ]
