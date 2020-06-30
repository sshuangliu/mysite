from django.shortcuts import render
from django.http import HttpResponse
from learn.models import CMDB_ASSET
from learn.forms import Device_infor, Device_update, UserForm
from django.http import HttpResponseRedirect
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate, login, logout
import csv,codecs
from django.http import FileResponse
from datetime import datetime
import os
# Create your views here.

# coding:utf-8

def test(request):
    return render(request, 'test.html')

def app_login(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            next_url = request.GET.get('next', '/mainpage')
            return HttpResponseRedirect(next_url)

        else:
            return render(request, 'login.html', {'form': form, 'error': '用户名或密码错误'})
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect('/mainpage')

        else:
            form = UserForm()
            return render(request, 'login.html', {'form': form})


def app_logout(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login')

@login_required()
def download(request, asset):
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录
    print(root_path)
    if asset == 'asset_list':
        new_path = os.path.join(root_path, 'media')
        print(new_path)
        filename = 'asset_list' + '_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.csv'
        asset_all = CMDB_ASSET.objects.all()    
        with codecs.open(os.path.join(new_path, filename), 'w', encoding='utf_8_sig') as csvfile:
            fieldnames = [
                'device_name', 
                'manage_ip',
                'produce',
                'os_software_version',
                'device_type',
                'serial_number',
                'login_u_p',
                'location',
                'warranty_expiration',
                'service_contract',
                'last_modification_timestamp',
                'initialization_timestamp',
                'comments',
                'device_op',
                ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in asset_all:
                writer.writerow({
                    'device_name': item.device_name,
                    'manage_ip': item.manage_ip,
                    'produce': item.produce,
                    'os_software_version': item.os_software_version,
                    'device_type': item.device_type,
                    'serial_number': item.serial_number,
                    'login_u_p': item.login_u_p,
                    'location': item.location,
                    'warranty_expiration': item.warranty_expiration,
                    'service_contract': item.service_contract,
                    'initialization_timestamp': item.initialization_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    'last_modification_timestamp': item.last_modification_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    'comments': item.comments, 
                    'device_op': '正常(Normal)' if item.device_op else '已删除(Deleted)' , 

                    })

        file=open(os.path.join(new_path, filename),'rb')
        response = FileResponse(file)
        response['Content-Type']='text/csv'
        response['Content-Disposition']=f'attachment;filename={filename}'
        return response

@login_required()
def index(request):
	return HttpResponseRedirect('/mainpage')


@login_required()
def topology_view(request):
    return render(request, 'OMS_BBY.html')

    
@login_required()
def mainpage(request):
    return render(request, 'mainpage.html')

@login_required()   
def device_select(request, successmessage=None, errormessage=None):
	base_infor = CMDB_ASSET.objects.filter(device_op=True)
	print(base_infor)
	cmdb_asset_all = [
        {'device_id': item.id,
    	 'device_name': item.device_name,
         'manage_ip': item.manage_ip,
         'produce': item.produce,
         'os_software_version': item.os_software_version,
         'device_type': item.device_type,
         'serial_number': item.serial_number,
         'login_u_p': item.login_u_p,
         'location': item.location,
         'warranty_expiration': item.warranty_expiration,
         'service_contract': item.service_contract,
         'initialization_timestamp': item.initialization_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
         'last_modification_timestamp': item.last_modification_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
         'comments': item.comments
         } for item in base_infor]
	return render(request, 'device_select.html',
    	{'cmdb_asset_all': cmdb_asset_all, 'successmessage': successmessage, 'errormessage': errormessage})


@login_required()
def device_add(request, successmessage=None, errormessage=None):
	form = Device_infor()
	if request.method == 'GET':
		return render(request, 'device_add.html', {'form': form})
	elif request.method == 'POST':
		form_post = Device_infor(request.POST)
    	# 包含POST数据的form，非空表单

        # A Form instance has an is_valid() method, which runs validation routines for all its fields. When this method is called, if all fields contain valid data, it will:
        #
        # return True
        # place the form’s data in its cleaned_data attribute.
		if form_post.is_valid():  # 调用clear函数去后台检查约束条件，有两个动作去执行
			device_base = CMDB_ASSET(
                               device_name=request.POST.get('device_name'),
                               manage_ip=request.POST.get('manage_ip'),
                               produce=request.POST.get('produce'),
                               os_software_version=request.POST.get('os_software_version'),
                               device_type=request.POST.get('device_type'),
                               serial_number=request.POST.get('serial_number'),
                               login_u_p=request.POST.get('login_u_p'),
                               location=request.POST.get('location'),
                               warranty_expiration=request.POST.get('warranty_expiration'),
                               service_contract=request.POST.get('service_contract'),
                               comments=request.POST.get('comments'),
                               )
			device_base.save()
			return render(request, 'device_add.html', {'form': form, 'successmessage': '设备添加完成!'})
		else:
			return render(request, 'device_add.html', {'form': form_post})  # 如果clear函数后台校验不通过，则把数据原封不动返回


@login_required()
def device_update(request, device_id, successmessage=None, errormessage=None):
	if request.method == 'GET':
		#try:  # 多人操作时，在查询界面上，A删除后，B没有刷新页面，编辑不存在的设备时 DoesNotExist的捕获
		item = CMDB_ASSET.objects.get(id=device_id)
		if item.device_op == True:  #条目逻辑删除(置为false), 条目一直存在，不会产生DoesNotExist的的异常
			init_form = Device_update(initial={
			'device_id': item.id,
			'device_name': item.device_name,
			'manage_ip': item.manage_ip,
			'produce': item.produce,
			'os_software_version': item.os_software_version,
			'device_type': item.device_type,
			'serial_number': item.serial_number,
			'login_u_p': item.login_u_p,
			'location': item.location,
			'warranty_expiration': item.warranty_expiration,
			'service_contract': item.service_contract,
			'comments': item.comments
			})

			return render(request, 'device_update.html', {'form': init_form, 'device_id': device_id})
		#except CMDB_ASSET.DoesNotExist:
		elif item.device_op == False:  # 条目逻辑删除(置为false)，条目一直存在，不会产生DoesNotExist的的异常
			return render(request, 'popup.html', {'infor': '此设备不存在或已被删除！!!'})

	elif request.method == 'POST':
		form_post = Device_update(request.POST)  # 包含POST数据的form，非空表单
		if form_post.is_valid():
            #try:  # 多人操作时，在update界面上 ，A删除后，B没有刷新页面，更新不存在的设备时 DoesNotExist的捕获
			item = CMDB_ASSET.objects.get(id=device_id)
			if item.device_op == True:
				item.device_name = request.POST.get('device_name')
				item.manage_ip = request.POST.get('manage_ip')
				item.produce = request.POST.get('produce')
				item.os_software_version = request.POST.get('os_software_version')
				item.device_type = request.POST.get('device_type')
				item.serial_number = request.POST.get('serial_number')
				item.login_u_p = request.POST.get('login_u_p')
				item.location = request.POST.get('location')
				item.warranty_expiration = request.POST.get('warranty_expiration')
				item.service_contract = request.POST.get('service_contract')
				item.comments = request.POST.get('comments')
				item.save()

				return render(request, 'popup.html', {'infor': 'update success!'})
			elif item.device_op == False:
				return render(request, 'popup.html', {'infor': '此设备不存在或已被删除！!'})
		else:
			return render(request, 'device_update.html', {'form': form_post})


@login_required()
def device_del(request, device_id):
    try:
        del_item = CMDB_ASSET.objects.get(id=device_id)
        del_item.device_op = False
        del_item.save()
        return render(request, 'popup.html', {'infor': 'delete success!'})
    except OPRS_DB.DoesNotExist:
        return render(request, 'popup.html', {'infor': '此设备不存在或已被删除！!'})
