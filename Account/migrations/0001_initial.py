# Generated by Django 3.0.3 on 2020-02-11 11:36

import Account.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Farmer',
            fields=[
                ('farmer_id', models.UUIDField(default=uuid.uuid4, help_text="Farmer's Unique ID", primary_key=True, serialize=False, unique=True, verbose_name="Farmer's ID")),
                ('farmer_full_name', models.CharField(help_text="Farmer's Full Name", max_length=100, verbose_name="Farmer's Fullname")),
                ('farmer_gender', models.CharField(choices=[('female', 'Female'), ('male', 'Male'), ('other', 'Other')], default='male', max_length=20, verbose_name="Farmer's Gender")),
                ('farmer_email', models.EmailField(blank=True, help_text="Farmer's Digital Point Of Contact", max_length=254, null=True, verbose_name="Farmer's Email")),
                ('farmer_verified_email', models.BooleanField(default=False, verbose_name="Farmer's Email Verified")),
                ('farmer_phone', models.CharField(max_length=10, validators=[Account.models.validate_phone_number], verbose_name="Farmer's Phone Number")),
                ('farmer_verified_phone', models.BooleanField(default=False, verbose_name="Farmer's Phone Verified")),
                ('farmer_doj', models.DateTimeField(auto_now_add=True, help_text='When did the farmer Created The Account', verbose_name='D.O.J')),
                ('farmer_dp', models.ImageField(default='dp/default.jpg', upload_to=Account.models.farmer_dp_upload, verbose_name="Farmer's Profile Pic")),
                ('farmer_user_auth', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="Famer's Authentication Account")),
            ],
            options={
                'verbose_name': 'Farmer',
                'verbose_name_plural': 'Farmers',
            },
        ),
    ]
