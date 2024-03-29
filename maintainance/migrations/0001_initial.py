# Generated by Django 4.1.7 on 2023-05-03 12:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('presale', '0008_alter_supplier_memo'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaintainanceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=1000)),
                ('date', models.DateField()),
                ('device', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='presale.device')),
                ('maintainer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
