"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from learn import views as learn_views

urlpatterns = [
    # login/logout
    path('accounts/login/', learn_views.app_login),
    path('accounts/logout/', learn_views.app_logout),

    path('admin/', admin.site.urls),

    path('', learn_views.index, name ='index'),
    path('mainpage/',learn_views.mainpage, name ='mainpage'),
    path('device_select/', learn_views.device_select, name='device_select'),
    path('device_add/', learn_views.device_add, name='device_add'),
    path('device_update/<int:device_id>', learn_views.device_update, name='device_update'),
    path('device_del/<int:device_id>', learn_views.device_del, name='device_del'),
    path('download/<str:asset>', learn_views.download, name='download'),
]
