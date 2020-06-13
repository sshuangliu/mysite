# mysite_cmdb_demo
GitHub supports emoji!
:+1: :sparkles: :camel: :tada:
:rocket: :metal: :octocat:

##### 介绍
自己练手的一个基于Django web项目 （入门教程可以参考这个：https://code.ziqiangxuetang.com/django/django-tutorial.html

目前上线 IT资产管理系统，增删查改，后续会慢慢增加其他功能：监控&告警，备份&巡检，IPDB（ip地址资源管理），设备配置（netconf rest api方式），集成Draw.io到本地，等其他小工具

前端参考了一个开源项目，觉得挺酷的，而且我不太熟悉前端技术，搬运了这个项目的部分前端代码，有些用不上功能的前端代码，不知啥意思，也粘上去了

[ansible-cmdb](https://github.com/fboender/ansible-cmdb)
##### 环境
Django 3.x
python 3.x

##### 安装项目到本地（Windows为例，Linux基本相同）
* 配置虚拟环境venv（与本地python环境隔离）
~~~
...\> py -m venv project-name
...\> project-name\Scripts\activate.bat 激活虚拟环境
~~~
* 安装Django（在虚拟环境下安装）默认安装源 卡的一比，自己搜索去换个或者全局代理后科学安装
~~~
...\> py -m pip install Django
...\> django-admin --version 验证你安装的 Django
~~~
* clone项目到本地（默认clone到该操作所在目录）请先单独安装git
~~~
git clone git@github.com:sshuangliu/mysite.git
~~~
* 运行该项目（在虚拟环境下）管理员用户信息（包括Django后台） admin/123456
~~~
cd 项目所在根目录
python manage.py runserver
 
# 当提示端口被占用的时候，可以用其它端口：
python manage.py runserver 8001
python manage.py runserver 9999
control-c 退出
 
# 监听机器所有可用 ip （电脑可能有多个内网ip或多个外网ip）
python manage.py runserver 0.0.0.0:8000
# 如果是外网或者局域网电脑上可以用其它电脑查看开发服务器
# 访问对应的 ip加端口，比如 http://172.16.20.2:8000
~~~

##### Screenshot

![image](https://github.com/sshuangliu/mysite/blob/master/readmeImage/login.png)

![image](https://github.com/sshuangliu/mysite/blob/master/readmeImage/asset.png)

![image](https://github.com/sshuangliu/mysite/blob/master/readmeImage/device_add.png)


