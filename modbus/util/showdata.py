
import logging
import json

from django_eventstream import send_event
from django.core.cache import cache
from modbus.modbus_config import Constant_config as cc
from modbus.monitor.monitor import doMonitor


def show_data():
    '''
    把取到的数据显示到页面上
    '''
    # 从redis 中获取数据

    datas = cache.get(cc.PLC_VALUE_KEY)
    if not datas:
        logging.info("还没有采集到数据！")
        return
    show_list1 = []

    for item in datas:

        show_item = {}
        show_item["device_name"] = item["device_name"]
        show_item["sensor_name"] = item["sensor_name"]
        show_item["sensor_value"] = item["sensor_value"]
        show_item["sensor_unit"] = item["sensor_unit"]
        show_item['adjust_value'] = item['adjust_value']
        show_item["data_time"] = item["data_time"]
        show_list1.append(show_item)
    logging.info("开始数据显示。")
    send_event('time', 'message', show_list1)
    monitor_data = doMonitor()
    send_event('monitor', 'message', json.dumps(monitor_data))
