# Generated by Django 3.0.3 on 2020-02-17 09:18

import Account.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Account', '0017_expertapply'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expert',
            fields=[
                ('expert_id', models.UUIDField(default=uuid.uuid4, help_text="Expert's Unique ID", primary_key=True, serialize=False, unique=True, verbose_name="Expert's ID")),
                ('expert_full_name', models.CharField(help_text="Expert's Full Name", max_length=100, verbose_name="Expert's Fullname")),
                ('expert_gender', models.CharField(choices=[('female', 'Female'), ('male', 'Male'), ('other', 'Other')], default='male', max_length=20, verbose_name="Expert's Gender")),
                ('expert_email', models.EmailField(help_text="Expert's Digital Point Of Contact", max_length=254, unique=True, verbose_name="Expert's Email")),
                ('expert_verified_email', models.BooleanField(default=False, verbose_name="Expert's Email Verified")),
                ('expert_phone', models.CharField(max_length=10, unique=True, validators=[Account.models.validate_phone_number], verbose_name="Expert's Phone Number")),
                ('expert_verified_phone', models.BooleanField(default=False, verbose_name="Expert's Phone Verified")),
                ('expert_plot_no', models.CharField(blank=True, default='', help_text="Expert's Plot No", max_length=50, verbose_name='Plot No')),
                ('expert_street', models.CharField(help_text="Expert's Street", max_length=150, verbose_name='Steet')),
                ('expert_landmark', models.CharField(blank=True, help_text="Expert's Landmark", max_length=100, null=True, verbose_name='Landmark')),
                ('expert_place', models.CharField(help_text="Expert's Palces", max_length=70, verbose_name='Places')),
                ('expert_city', models.CharField(help_text="Expert's City", max_length=60, verbose_name='City')),
                ('expert_state', models.CharField(help_text="Expert's State", max_length=70, verbose_name='State')),
                ('expert_country', models.CharField(help_text="Expert's Counrty", max_length=50, verbose_name='Country')),
                ('expert_dp', models.ImageField(default='dp/default.jpg', upload_to=Account.models.farmer_dp_upload, verbose_name="Expert's Profile Pic")),
                ('expert_user_auth', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='expert_account', to=settings.AUTH_USER_MODEL, verbose_name="Famer's Authentication Account")),
            ],
            options={
                'verbose_name': 'Expert',
                'verbose_name_plural': 'Experts',
            },
        ),
    ]