# Generated by Django 4.0.3 on 2022-05-19 10:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0024_alter_shopuser_activation_key_expires'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuserprofile',
            name='tagline',
            field=models.CharField(blank=True, max_length=128, verbose_name='тэги'),
        ),
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 5, 21, 10, 26, 22, 740611), null=True),
        ),
        migrations.AlterField(
            model_name='shopuserprofile',
            name='about',
            field=models.TextField(blank=True, max_length=512, null=True, verbose_name='О себе'),
        ),
        migrations.AlterField(
            model_name='shopuserprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Мужчина'), ('W', 'Женщина')], max_length=1, verbose_name='пол'),
        ),
    ]
