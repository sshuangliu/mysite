import django
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# 让任何一个Py文件都能加载Django项目的models模块

from learn.models import CMDB_ASSET, IP_monitor
import zmail
from datetime import datetime, timedelta
import threading
import time

class notice:

    def __init__(self):
        self.email_context = []


    def to_be_notice(self, db):
            if db.online_or_not == False and db.sent_or_not == False and db.monitor_or_not == True:
                db.sent_or_not = True
                db.last_sent_time = datetime.now()
                db.save()
                self.email_context.append({'manage_ip': db.manage_ip, 'device_name': CMDB_ASSET.objects.get(manage_ip=db.manage_ip).device_name})
            if db.online_or_not == False and db.sent_or_not == True and db.monitor_or_not == True and (datetime.now() - timedelta(days=1))> db.last_sent_time:
                db.last_sent_time = datetime.now()
                db.save()
                self.email_context.append({'manage_ip': db.manage_ip, 'device_name': CMDB_ASSET.objects.get(manage_ip=db.manage_ip).device_name})

    def my_send_mail(self):
        self.threading_tbn()
        if self.email_context:
            msg = 'Important notice:\n\n\nPlease check below devices'
            for i in self.email_context:
                msg = msg + i['device_name'] + '\t' + i['manage_ip'] + '\n'
            print(msg)
            mail = {
                'subject': 'Important notice: BBY China Monitor alert',  # Anything you want.
                'content_text': msg # Anything you want.
                # 'attachments': ['/Users/zyh/Documents/example.zip','/root/1.jpg'],  # Absolute path will be better.
                }
            server = zmail.server('904680136@qq.com', 'xcpscbxggnrqbdfc')
            server.send_mail('aa340261@bestbuy.com', mail)
            # server.send_mail(['foo@163.com','foo@126.com'],mail,cc=['bar@163.com'])


    def threading_tbn(self):
        start = time.perf_counter()
        ip_monitor_base = IP_monitor.objects.all()
        thread_list = [threading.Thread(target=self.to_be_notice, args=(item,)) for item in ip_monitor_base]
        for t in thread_list:
            t.start()
        for t in thread_list:
            if t.is_alive():
                t.join()

        #print(threading.active_count())
        print()
        print("all done: time", time.perf_counter() - start, "\n")


if __name__ == '__main__':
    my_notice = notice()
    my_notice.my_send_mail()
    # my_notice.threading_tbn()