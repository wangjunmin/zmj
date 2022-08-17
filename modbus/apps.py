
import logging
import threading
import time
from django.apps import AppConfig

from modbus.modbus_config import Constant_config


class ModbusConfig(AppConfig):
    '''
    增加多个设备支持。0811
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modbus'

    def ready(self):
        ensure_worker_started()


worker_started = False


def ensure_worker_started():
    global worker_started

    if worker_started:
        return

    if not is_db_ready():
        return

    worker_started = True
    print("开始执行数据采集任务")

    thread_id = 1
    get_all_devices()

    for device_item in Constant_config.device_list:
        thread = col_thread(threadID=thread_id, device_name=device_item[0],
                            time_interval=device_item[1])
        thread.daemon = True
        thread.start()
        thread_id += 1

    show_thread = threading.Thread(target=show_worker)
    show_thread.daemon = True
    show_thread.start()


def get_all_devices():
    from modbus.models import DeviceInfo
    devices = DeviceInfo.objects.all()
    Constant_config.device_list = []
    for device_item in devices:
        Constant_config.device_list.append(
            (device_item.name, device_item.time_interval))


def show_worker():
    from modbus.util.showdata import show_data
    while True:
        show_data()
        time.sleep(Constant_config.COL_INTERVAL)


def is_db_ready():
    from django.db import DatabaseError
    from django_eventstream.models import Event

    try:
        # see if db tables are present
        Event.objects.count()
        return True
    except DatabaseError:
        return False


class col_thread(threading.Thread):
    '''
    数据采集线程对象
    '''

    def __init__(self, device_name, time_interval, threadID) -> None:
        threading.Thread.__init__(self)
        self.device_name = device_name
        self.time_interval = time_interval
        self.threadID = threadID

    def run(self):
        from modbus.tasks import collect_data, insert_his
        while True:
            time.sleep(self.time_interval)
            collect_data(self.device_name)
            # 根据配置信息决定是否写入数据库。
            if Constant_config.switch_his:
                insert_his()
