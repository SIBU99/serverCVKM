# Generated by Django 3.0.3 on 2020-02-17 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0015_auto_20200217_1321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otptokenphone',
            name='changed_tracker',
        ),
    ]
