# Generated by Django 4.1.2 on 2023-03-14 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_demolandcoverclassificationtask_demo_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='demolandcoverclassificationtask',
            name='status_long_message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='forestchangetask',
            name='status_long_message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
