from django.contrib import admin

# Register your models here.
from learn.models import CMDB_ASSET, IP_monitor

admin.site.register(CMDB_ASSET)
admin.site.register(IP_monitor)