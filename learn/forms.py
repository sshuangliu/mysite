# Django form field types
# https://www.webforefront.com/django/formfieldtypesandvalidation.html

from django import forms
from django.core.validators import RegexValidator
from learn.models import CMDB_ASSET


# 添加设备的表单
class Device_infor(forms.Form):
    # 必填表单前* 调用js
	required_css_class = 'required' 

	device_name = forms.CharField(max_length=50,
                                  required=True,
                                  label='设备名(device_name)',
                                  widget=forms.TextInput(attrs={'class': "form-control"})
                                  )

	manage_ip = forms.GenericIPAddressField(required=False,
                                                label='管理IP(manage_ip)',
                                                widget=forms.TextInput(
                                                    attrs={'class': "form-control", "placeholder": "ipv4 or ipv6:"})
                                                )

	produce = forms.CharField(max_length=50,
                                    required=True,
                                    label='产品型号(produce)',
                                    widget=forms.TextInput(attrs={'class': "form-control"})
                                    )

	os_software_version = forms.CharField(max_length=50,
                                    required=False,
                                    label='系统&软件版本(os_software_version)',
                                    widget=forms.TextInput(attrs={'class': "form-control"})
                                    )

	type_choices = (
        ('router', '路由器(router)'), ('switch', '交换机(switch)'), ('switch-stack', '交换机堆叠(switch-stack)'), ('server', '服务器(server)'), ('voice_video', '音视频设备(voice_video)'), ('other', '其他(other)'), ('app_server', '应用服务(app_server)'))  # 表单约束，只能选择给定，和数据库表值约束匹配
	device_type = forms.CharField(required=True,
                                  label='设备类型(device_type)',
                                  widget=forms.Select(choices=type_choices, attrs={'class': "form-control"})
                                  )

	sn_regex = RegexValidator(regex=r'^\S*$',
                              message="SN must be ....not null")  # 校验失败的消息会通过form.errow推送
	serial_number = forms.CharField(validators=[sn_regex],
                                max_length=30,
                                min_length=8,
                                required=False,
                                label='序列号(serial_number)',
                                widget=forms.TextInput(
                                    attrs={'class': "form-control"})
                                )

	login_u_p = forms.CharField(max_length=50,
                                    required=False,
                                    label='登录信息(login_u_p)',
                                    widget=forms.TextInput(attrs={'class': "form-control"})
                                    )

	location_choices = (
        ('SH-HQ', 'SH-HQ'), ('SH-IDC', 'SH-IDC'), ('SZ', 'SZ'), ('TW', 'TW'))  # 表单约束，只能选择给定，和数据库表值约束匹配
	location = forms.CharField(required=True,
                                  label='设备区域(location)',
                                  widget=forms.Select(choices=location_choices, attrs={'class': "form-control"})
                                  )

	warranty_expiration = forms.CharField(max_length=50,
                                    required=False,
                                    label='维保日期(warranty_expiration)',
                                    widget=forms.TextInput(attrs={'class': "form-control"})
                                    )

	service_contract = forms.CharField(max_length=50,
                                    required=False,
                                    label='维保联系方式(service_contract)',
                                    widget=forms.TextInput(attrs={'class': "form-control"})
                                    )

	comments = forms.CharField(required=False,
							label='备注(comments)',
							widget=forms.Textarea(attrs={'class': "form-control"}))


	def clean(self):  # 表单的验证，用于多字段依懒性验证
		cleaned_data = super().clean()
		device_type = self.cleaned_data.get('device_type')
		device_name = self.cleaned_data['device_name']
		manage_ip = self.cleaned_data.get('manage_ip')
		print(f'device_name={device_name}')
		print(f'device_type={device_type}')
		print(f'manage_ip={manage_ip}')
		if device_type != 'switch-stack':
			if CMDB_ASSET.objects.filter(device_name=device_name).exists() or \
				(manage_ip !='' and CMDB_ASSET.objects.filter(manage_ip=manage_ip).exists()):
				msg = "device_name or manage_ip can't duplicate when device_type is none switch-stack"
				msg2 = ''
				self.add_error('device_name', msg)  # 将error信息分配给一个指定field,fidle字段级别error
				self.add_error('manage_ip', msg)
				#raise forms.ValidationError("device_name or manage_ip can't dup when device_type is none switch-stack")  # form级别error




	def clean_serial_number(self):
		serial_number = self.cleaned_data.get('serial_number')
		if serial_number != '' and CMDB_ASSET.objects.filter(serial_number=serial_number).exists():
			raise forms.ValidationError('serial_number已存在！')  # 抛出异常到form.字段.errow 类
		return serial_number


class Device_update(forms.Form):

	# 必填表单前* 调用js
	required_css_class = 'required'

	device_id = forms.IntegerField(label='设备唯一ID(device_id)',
	                               widget=forms.NumberInput(attrs={'class': "form-control", 'readonly': True}))

	device_name = forms.CharField(max_length=50,
	                              required=True,
                                  label='设备名(device_name)',
                                  widget=forms.TextInput(attrs={'class': "form-control"})
                                  )

	manage_ip = forms.GenericIPAddressField(required=False,
                                                label='管理IP(manage_ip)',
                                                widget=forms.TextInput(
                                                    attrs={'class': "form-control", "placeholder": "ipv4 or ipv6:"})
                                                )

	produce = forms.CharField(max_length=50,
                                    required=True,
                                    label='产品型号(produce)',
                                    widget=forms.TextInput(attrs={'class': "form-control"})
                                    )

	os_software_version = forms.CharField(max_length=50,
                                    required=False,
                                    label='系统&软件版本(os_software_version)',
                                    widget=forms.TextInput(attrs={'class': "form-control"})
                                    )

	type_choices = (
        ('router', '路由器(router)'), ('switch', '交换机(switch)'), ('switch-stack', '交换机堆叠(switch-stack)'), ('server', '服务器(server)'), ('voice_video', '音视频设备(voice_video)'), ('other', '其他(other)'), ('app_server', '应用服务(app_server)'))  # 表单约束，只能选择给定，和数据库表值约束匹配
	device_type = forms.CharField(required=True,
                                  label='设备类型(device_type)',
                                  widget=forms.Select(choices=type_choices, attrs={'class': "form-control"})
                                  )

	sn_regex = RegexValidator(regex=r'^\S*$',
                              message="SN must be ....not null")  # 校验失败的消息会通过form.errow推送
	serial_number = forms.CharField(validators=[sn_regex],
                                max_length=30,
                                min_length=8,
                                required=False,
                                label='序列号(serial_number)',
                                widget=forms.TextInput(
                                    attrs={'class': "form-control"})
                                )

	login_u_p = forms.CharField(max_length=50,
                                    required=False,
                                    label='登录信息(login_u_p)',
                                    widget=forms.TextInput(attrs={'class': "form-control"})
                                    )

	location_choices = (
        ('SH-HQ', 'SH-HQ'), ('SH-IDC', 'SH-IDC'), ('SZ', 'SZ'), ('TW', 'TW'))  # 表单约束，只能选择给定，和数据库表值约束匹配
	location = forms.CharField(required=True,
                                  label='设备区域(location)',
                                  widget=forms.Select(choices=location_choices, attrs={'class': "form-control"})
                                  )

	warranty_expiration = forms.CharField(max_length=50,
                                    required=False,
                                    label='维保日期(warranty_expiration)',
                                    widget=forms.TextInput(attrs={'class': "form-control"})
                                    )

	service_contract = forms.CharField(max_length=50,
                                    required=False,
                                    label='维保联系方式(service_contract)',
                                    widget=forms.TextInput(attrs={'class': "form-control"})
                                    )

	comments = forms.CharField(required=False,
							label='备注(comments)',
							widget=forms.Textarea(attrs={'class': "form-control"}))

	def clean(self):
		cleaned_data = super().clean()
		device_name = self.cleaned_data.get('device_name')
		device_id = self.cleaned_data.get('device_id')
		device_type = self.cleaned_data.get('device_type')
		manage_ip = self.cleaned_data.get('manage_ip')
		print(f'device_name{device_name}')
		print(f'device_id{device_id}')
		print(f'device_type{device_type}')
		print(f'manage_ip{manage_ip}')
		if device_type != 'switch-stack':
			if [item for item in CMDB_ASSET.objects.filter(device_name=device_name) if item.id != int(device_id)] or \
			[item for item in CMDB_ASSET.objects.filter(manage_ip=manage_ip) if item.id != int(device_id)]:
			 # if为false，即查不到信息时，不一定完全正确，可能是一个已被删除(物理删除，非逻辑删除)的设备，最终判断交给view device_update主函数
				msg = "device_name or manage_ip can't duplicate when device_type is none switch-stack"
				msg2 = ''
				self.add_error('device_name', msg)  # 将error信息分配给一个指定field,fidle字段级别error
				self.add_error('manage_ip', msg)

	'''
	def clean_device_name(self):
		device_name = self.cleaned_data.get('device_name')
		device_id = self.cleaned_data.get('device_id')
		device_type = self.cleaned_data.get('device_type')
		manage_ip = self.cleaned_data.get('manage_ip')
		print(f'device_name{device_name}')
		print(f'device_id{device_id}')
		print(f'device_type{device_type}')
		print(f'manage_ip{manage_ip}')
		if device_type != 'switch-stack':
			if [item for item in CMDB_ASSET.objects.filter(device_name=device_name) if
			item.id != int(device_id)]:  # if为false，即查不到信息时，不一定完全正确，可能是一个已被删除的设备，最终判断交给view device_update主函数
				raise forms.ValidationError("device_name or manage_ip can't duplicate when device_type is none switch-stack！")  # 抛出异常到form.error 类
		return device_name

	def clean_manage_ip(self):
		manage_ip = self.cleaned_data.get('manage_ip')
		device_id = self.cleaned_data.get('device_id')
		device_type = self.cleaned_data.get('device_type')
		print(f'manage_ip{manage_ip}')
		if device_type != 'switch-stack':
			if [item for item in CMDB_ASSET.objects.filter(manage_ip=manage_ip) if
				item.id != int(device_id)]:  # if为false，即查不到信息时，不一定完全正确，可能是一个已被删除的设备，最终判断交给view device_update主函数
				raise forms.ValidationError("device_name or manage_ip can't duplicate when device_type is none switch-stack！")  # 抛出异常到form.error 类
		return manage_ip

	'''
	def clean_serial_number(self):
		serial_number = self.cleaned_data.get('serial_number')
		device_id = self.cleaned_data.get('device_id')
		if serial_number != '':
			if [item for item in CMDB_ASSET.objects.filter(serial_number=serial_number) if
				item.id != int(device_id)]:  # if为false，即查不到信息时，不一定完全正确，可能是一个已被删除的设备，最终判断交给view device_update主函数
				raise forms.ValidationError('serial_number已存在！')  # 抛出异常到form.字段.errow 类
		return serial_number


class UserForm(forms.Form):
	username = forms.CharField(label=False,
                               max_length=10,
                               required=True,
                               widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username: "})
                               )
	password = forms.CharField(label=False,
                               max_length=100,
                               required=True,
                               widget=forms.PasswordInput(
                                   attrs={"class": "form-control", "placeholder": "Password: "})
                               )