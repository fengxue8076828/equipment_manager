# Generated by Django 4.1.7 on 2023-04-19 12:15

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('postsale', '0003_devicesold_state_alter_devicesold_outbound_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicesold',
            name='buyer',
        ),
        migrations.RemoveField(
            model_name='devicesold',
            name='outbound_date',
        ),
        migrations.RemoveField(
            model_name='devicesold',
            name='outbound_image',
        ),
        migrations.RemoveField(
            model_name='devicesold',
            name='outbound_operator',
        ),
        migrations.RemoveField(
            model_name='devicesold',
            name='pay_date',
        ),
        migrations.RemoveField(
            model_name='devicesold',
            name='pay_state',
        ),
        migrations.CreateModel(
            name='OutBound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outbound_number', models.CharField(max_length=100)),
                ('outbound_date', models.DateField()),
                ('outbound_image', models.ImageField(upload_to='outbound-images/')),
                ('pay_state', models.CharField(choices=[('paid', '已结算'), ('unpaid', '未结算')], max_length=30)),
                ('pay_date', models.DateField(default=datetime.date(2023, 4, 19))),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='devices_bought', to='postsale.client')),
                ('outbound_operator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='devices_sold', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='devicesold',
            name='outbound',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='postsale.outbound'),
        ),
    ]
