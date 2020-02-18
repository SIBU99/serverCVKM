# Generated by Django 3.0.3 on 2020-02-18 18:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0024_others_other_dp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expertapply',
            name='applicant_supported_docs',
        ),
        migrations.AddField(
            model_name='expert',
            name='expert_doj',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name="Expert's D.O.J."),
            preserve_default=False,
        ),
    ]
