# Generated by Django 3.0.3 on 2020-02-12 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0004_auto_20200212_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmer',
            name='farmer_social_auth_provider',
            field=models.CharField(choices=[('google-oauth2', 'Google'), ('facebook', 'Facebook'), (None, 'Manual Registration')], max_length=50, null=True, verbose_name="Farmer's Social Auth Provider"),
        ),
    ]