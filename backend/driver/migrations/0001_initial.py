# Generated by Django 4.1.6 on 2023-03-21 18:38

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0004_alter_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('carId', models.CharField(default='NA', max_length=256)),
                ('carModel', models.CharField(default='NA', max_length=256)),
                ('carNumber', models.CharField(default='Na', max_length=256)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'abstract': False,
            },
            bases=('authentication.user',),
        ),
    ]