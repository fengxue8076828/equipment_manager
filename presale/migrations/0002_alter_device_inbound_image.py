# Generated by Django 4.1.7 on 2023-04-11 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presale', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='inbound_image',
            field=models.ImageField(upload_to='inbound-images/'),
        ),
    ]
