# Generated by Django 5.2.1 on 2025-06-17 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cardboard_production', '0003_density_alter_material_density'),
    ]

    operations = [
        migrations.AddField(
            model_name='productions',
            name='order_status',
            field=models.IntegerField(choices=[(0, 'В очереди'), (1, 'В производстве'), (2, 'Изготовленно')], default=0, verbose_name='Статус заказа'),
        ),
    ]
