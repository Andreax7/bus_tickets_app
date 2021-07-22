# Generated by Django 3.1.5 on 2021-07-12 05:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_api', '0004_auto_20210704_0314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='single_ticket',
            name='Profiles_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='single_ticket',
            name='non_users_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_api.non_users'),
        ),
    ]
