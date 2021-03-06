# Generated by Django 3.0.7 on 2020-06-08 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0003_auto_20200608_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cmdb_asset',
            name='initialization_timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='录入时间'),
        ),
        migrations.AlterField(
            model_name='cmdb_asset',
            name='last_modification_timestamp',
            field=models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间'),
        ),
    ]
