# Generated by Django 4.1.7 on 2023-04-26 11:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('presale', '0004_equipment_sale_price_alter_equipment_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inbound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inbound_number', models.CharField(max_length=100)),
                ('inbound_date', models.DateField()),
                ('inbound_image', models.ImageField(upload_to='inbound-images/')),
                ('inbound_operator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='devices_inbound', to=settings.AUTH_USER_MODEL)),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='devices_supplier', to='presale.suppier')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='inbount',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='presale.inbound'),
        ),
    ]
