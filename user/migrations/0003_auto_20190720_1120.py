# Generated by Django 2.2.3 on 2019-07-20 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.IntegerField(choices=[(0, '未知'), (1, '男'), (2, '女')], default=0),
        ),
    ]
