# Generated by Django 5.2.1 on 2025-07-01 08:49

import cardboard_production.custom_validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cardboard_production', '0012_alter_cuttingcardboard_order1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='file',
            field=models.FileField(blank=True, default=None, null=True, upload_to='Scheme/%Y/%m/', validators=[cardboard_production.custom_validator.custom_file_validator], verbose_name='Cхема'),
        ),
    ]
