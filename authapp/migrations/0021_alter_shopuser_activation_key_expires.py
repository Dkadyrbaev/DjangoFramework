# Generated by Django 4.0.3 on 2022-05-18 09:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0020_alter_shopuser_activation_key_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 5, 20, 9, 20, 21, 880902), null=True),
        ),
    ]
