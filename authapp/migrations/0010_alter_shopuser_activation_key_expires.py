# Generated by Django 4.0.3 on 2022-04-15 13:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0009_rename_userprofile_shopuserprofile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 17, 13, 8, 53, 853565), null=True),
        ),
    ]
