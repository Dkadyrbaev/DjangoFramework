# Generated by Django 4.0.3 on 2022-04-19 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basketapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='активна'),
        ),
    ]
