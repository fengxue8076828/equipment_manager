# Generated by Django 4.1.7 on 2023-05-10 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presale', '0008_alter_supplier_memo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='state',
            field=models.CharField(choices=[('ready_excellent', '可发货(好)'), ('ready_good', '可发货(中)'), ('ready', '可发货'), ('ready_confirm', '可发货，需确认'), ('bad', '故障'), ('maintaining', '检修中')], max_length=100),
        ),
    ]
