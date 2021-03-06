# Generated by Django 3.0.7 on 2020-06-08 04:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CMDB_ASSET',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(max_length=100, verbose_name='设备名')),
                ('manage_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='设备管理ip')),
                ('produce', models.CharField(max_length=100, verbose_name='设备型号')),
                ('os_software_version', models.CharField(max_length=100, verbose_name='软件&系统版本')),
                ('device_type', models.CharField(choices=[('router', '路由器'), ('switch', '交换机'), ('server', '服务器'), ('voice_video', '音视频设备'), ('other', '其他')], max_length=20)),
                ('serial_number', models.CharField(blank=True, max_length=30, unique=True, validators=[django.core.validators.RegexValidator(message='SN must be none NULL....', regex='^\\S*$')])),
                ('login_u_p', models.CharField(max_length=100, verbose_name='设备登录信息')),
                ('location', models.CharField(max_length=10, verbose_name='设备所属区域')),
                ('warranty_expiration', models.CharField(max_length=30, verbose_name='设备维保时间')),
                ('service_contract', models.CharField(max_length=30, verbose_name='设备维保服务联系方式')),
                ('initialization_timestamp', models.DateTimeField(auto_now=True, verbose_name='录入时间')),
                ('last_modification_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='最近一次修改时间')),
                ('comments', models.CharField(max_length=100, verbose_name='备注')),
                ('device_op', models.BooleanField(choices=[(True, '正常'), (False, '已删除')], default=True, verbose_name='设备是否删除')),
            ],
        ),
    ]
