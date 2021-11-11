import django
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# 让任何一个Py文件都能加载Django项目的models模块

from learn.models import CMDB_ASSET, IP_monitor
import threading
import time
import subprocess
from queue import Queue

WORD_THREAD = 50

IP_QUEUE = Queue()
for i in IP_monitor.objects.all():
	IP_QUEUE.put(i.manage_ip)


def live_monitor():
	while not IP_QUEUE.empty():
		ip = IP_QUEUE.get()
		# if the ip is alive,res = 0,otherwise res = 1
		res = subprocess.call(f'ping -n 2 -w 5 {ip}', stdout = subprocess.PIPE)
		if not res:
			print(f'{ip }: {res} True')
			ip_monitor_item = IP_monitor.objects.get(manage_ip=ip)
			ip_monitor_item.online_or_not = True
			ip_monitor_item.sent_or_not = False
			ip_monitor_item.save()
		else:
			print(f'{ip }: {res} False')
			ip_monitor_item = IP_monitor.objects.get(manage_ip=ip)
			ip_monitor_item.online_or_not = False
			ip_monitor_item.save()



if __name__ == '__main__':
	threads = []
	start = time.perf_counter()
	for i in range(WORD_THREAD):
		thread = threading.Thread(target=live_monitor)
		thread.start()
		threads.append(thread)

	for thread in threads:
		thread.join()

	print()
	print("all done: time", time.perf_counter() - start, "\n")

