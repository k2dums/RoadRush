# Generated by Django 4.1.6 on 2023-03-22 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0006_driver_occupied_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driver',
            old_name='occupied_status',
            new_name='occupiedStatus',
        ),
        migrations.AlterField(
            model_name='driver',
            name='carId',
            field=models.CharField(default='NA', max_length=256, unique=True),
        ),
    ]