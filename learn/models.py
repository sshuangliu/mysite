from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
# Create your models here.
# https://www.webforefront.com/django/modeldatatypesandvalidation.html
 
class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    
    def __str__(self):
        return self.name

# null : If True, Django will store empty values as NULL in the database. Default is False
# blank : If True, the field is allowed to be blank. Default is False
# unique : If True, this field must be unique throughout the table, Default is False
class CMDB_ASSET(models.Model):
    device_name = models.CharField(max_length=100, verbose_name='设备名', unique=False, blank=False)

    manage_ip = models.GenericIPAddressField(blank=True, null =True, unique=False, verbose_name='设备管理ip')

    produce = models.CharField(blank=True, max_length=100, verbose_name='设备型号')

    os_software_version = models.CharField(blank=True, max_length=100, verbose_name='软件&系统版本')

    # 设备类型,后面的为选择内容,前面为写入数据库的值, 注意max_length必须配置
    direction_choices = (('router', '路由器(router)'), ('switch', '交换机(switch)'), ('switch-stack', '交换机堆叠(switch-stack)'), ('server', '服务器(server)'), ('voice_video', '音视频设备(voice_video)'), ('other', '其他(other)'), ('app_server', '应用服务(app_server)'))  #  数据库表约束，只能写入给定选择，和表单值匹配
    device_type = models.CharField(max_length=30, choices=direction_choices)

    # SN,校验不包含空类型字符,最大长度为11,不可以为空,唯一键(注意:并没有min_length这个控制字段)
    sn_regex = RegexValidator(regex=r'^\S*$',
                              message="SN must be none NULL....")
    serial_number = models.CharField(blank=True, validators=[sn_regex], max_length=30, unique=False)

    login_u_p = models.CharField(blank=True, max_length=100, verbose_name='设备登录信息')

    location = models.CharField(max_length=10, verbose_name='设备所属区域')

    warranty_expiration = models.CharField(blank=True, max_length=30, verbose_name='设备维保时间')

    service_contract = models.CharField(blank=True, max_length=30, verbose_name='设备维保服务联系方式')

    # 最近一次资料更新时间,
    # use the auto_now option are updated every time a record is changed
    last_modification_timestamp = models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')

    # 初始化时间
    # auto_now_add option remain frozen for the lifetime of the record
    initialization_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='录入时间')

    # 备注
    comments = models.CharField(blank=True, max_length=100, verbose_name='备注')

    # 是否逻辑删除标记,后面的为选择内容,前面为写入数据库的值, 注意max_length必须配置
    tag = ((True, '正常'), (False, '已删除'))
    device_op = models.BooleanField(default=True, choices=tag, verbose_name='设备是否删除')

    def __str__(self):
        return f"{self.__class__.__name__}(device_name: {self.device_name} | manage_ip: {self.manage_ip} | produce: {self.produce} | os_software_version: {self.os_software_version} | device_type: {self.device_type} | serial_number: {self.serial_number} | login_u_p: {self.login_u_p} | location: {self.location} | warranty_expiration: {self.warranty_expiration} | service_contract: {self.service_contract} | initialization_timestamp: {self.initialization_timestamp} | last_modification_timestamp: {self.last_modification_timestamp} | comments: {self.comments} | device_op: {self.device_op})"



class IP_monitor(models.Model):
    manage_ip = models.GenericIPAddressField(blank=False, null =False, unique=True, verbose_name='设备管理_监控ip')
    
    tag1 = ((True, '连通'), (False, '不连通'))
    online_or_not = models.BooleanField(default=True, choices=tag1, verbose_name='设备IP是否连通')

    tag2 = ((True, 'enable'), (False, 'disable'))
    monitor_or_not = models.BooleanField(default=False, choices=tag2, verbose_name='设备IP是否监控')

    tag3 = ((True, '已发送'), (False, '未发送'))
    sent_or_not = models.BooleanField(default=False, choices=tag3, verbose_name='告警邮件是否发送')
    
    # Don't add () PARENTHESIS to methods in default values, while evaluates the expression at compile time rathe than at runtime
    last_sent_time = models.DateTimeField(default=timezone.now, verbose_name='最近一次邮件发送时间')

    def __str__(self):
        return f"{self.__class__.__name__}(manage_ip: {self.manage_ip} | online_or_not: {self.online_or_not} | monitor_or_not: {self.monitor_or_not} | sent_or_not: {self.sent_or_not} | last_sent_time: {self.last_sent_time})"

