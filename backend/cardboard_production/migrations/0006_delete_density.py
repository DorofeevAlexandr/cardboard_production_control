# Generated by Django 5.2.1 on 2025-06-17 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cardboard_production', '0005_alter_material_density_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Density',
        ),
    ]
