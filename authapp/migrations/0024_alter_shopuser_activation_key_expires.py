# Generated by Django 4.0.3 on 2022-05-19 09:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0023_alter_shopuser_activation_key_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 5, 21, 9, 26, 17, 629543), null=True),
        ),
    ]
