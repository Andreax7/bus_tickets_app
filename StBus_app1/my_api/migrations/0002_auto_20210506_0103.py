# Generated by Django 3.1.5 on 2021-05-05 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='destinations',
            name='dfrom',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='destinations',
            name='dto',
            field=models.CharField(max_length=64, null=True),
        ),
    ]