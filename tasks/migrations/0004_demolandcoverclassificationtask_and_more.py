# Generated by Django 4.1.2 on 2023-03-08 14:14

import SmartCarteApi.common
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_forestchangetask_after_rgb_tiles_href_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DemoLandcoverClassificationTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('datetime_created', models.DateTimeField(default=SmartCarteApi.common.get_utc_datetime_now)),
                ('datetime_completed', models.DateTimeField(null=True)),
                ('datetime_updated', models.DateTimeField(null=True)),
                ('type', models.CharField(max_length=40, null=True)),
                ('status', models.CharField(max_length=50)),
                ('status_message', models.CharField(blank=True, max_length=200, null=True)),
                ('date', models.DateField()),
                ('region_geojson', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('statistics_json', models.TextField()),
                ('imagery_tif_href', models.CharField(max_length=240, null=True)),
                ('imagery_tiles_href', models.CharField(max_length=240, null=True)),
                ('landcover_tif_href', models.CharField(max_length=240, null=True)),
                ('landcover_tiles_href', models.CharField(max_length=240, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='forestchangetask',
            name='status',
            field=models.CharField(max_length=50),
        ),
    ]