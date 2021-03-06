# Generated by Django 4.0.3 on 2022-04-20 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordersapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='create',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='update',
            new_name='updated',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[(1, 'Формируется'), (2, 'В обработке'), (3, 'Оплачен'), (4, 'Собирается'), (5, 'Готов'), (6, 'Отменён')], default=1, max_length=3, verbose_name='Статус'),
        ),
    ]
