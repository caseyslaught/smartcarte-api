# Generated by Django 4.1.2 on 2023-03-16 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_alter_demolandcoverclassificationtask_statistics_json'),
    ]

    operations = [
        migrations.AddField(
            model_name='demolandcoverclassificationtask',
            name='rgb_tif_href',
            field=models.CharField(blank=True, max_length=240, null=True),
        ),
    ]
