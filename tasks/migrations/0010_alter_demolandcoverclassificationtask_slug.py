# Generated by Django 4.1.2 on 2023-04-07 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_demolandcoverclassificationtask_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demolandcoverclassificationtask',
            name='slug',
            field=models.CharField(blank=True, max_length=40, null=True, unique=True),
        ),
    ]
