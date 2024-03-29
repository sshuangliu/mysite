# Generated by Django 3.0.7 on 2021-11-02 16:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0008_auto_20200610_1617'),
    ]

    operations = [
        migrations.CreateModel(
            name='IP_monitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manage_ip', models.GenericIPAddressField(unique=True, verbose_name='设备管理_监控ip')),
                ('online_or_not', models.BooleanField(choices=[(True, '连通'), (False, '不连通')], default=True, verbose_name='设备IP是否连通')),
                ('monitor_or_not', models.BooleanField(choices=[(True, 'enable'), (False, 'disable')], default=True, verbose_name='设备IP是否监控')),
                ('sent_or_not', models.BooleanField(choices=[(True, '已发送'), (False, '未发送')], default=True, verbose_name='告警邮件是否发送')),
                ('last_sent_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='最近一次邮件发送时间')),
            ],
        ),
    ]
