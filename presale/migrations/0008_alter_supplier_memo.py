# Generated by Django 4.1.7 on 2023-04-28 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presale', '0007_rename_suppier_supplier_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='memo',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
