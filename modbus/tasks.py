# Create your tasks here
from __future__ import absolute_import, unicode_literals

import logging
import time
import traceback

from modbus.models import PLC_His
from modbus.monitor.monitor import doExcept, doNormal

from modbus.util.modbusDriver import modbusDriver

from django.core.cache import cache

from modbus.util.mqtt_driver import MqttDriver
from .modbus_config import Constant_config as cc


def collect_data(device_name):
    '''
    采集数据的任务
    1. 任务内容包括从PLC获取数据
    2. 把获取的数据放到数据库中,为了性能，把写入数据库的操作移到订阅内容中去
    3. 把获取的实时数据放到redis中缓存起来
    '''

    try:

        driver = modbusDriver(device_name)
        t = time.time()
        datas = driver.get_values()
        push_redis(datas)
        pub_mqtt(device_name, datas)
        doNormal(cc.PLC_NORMAL)
        cc.col_interval_time = time.time()-t
    except Exception as e:
        print("运行过程中出错了:", str(e))
        traceback.print_exc()
        cc.err_message = str(e)

        # 采集值清零
        push_redis({})
        doExcept(cc.PLC_ERR, e)


def insert_his():
    '''
    把取到的数据写入数据库
    信息同步到前端显示
    '''
    # 从redis 中获取数据

    datas = cache.get(cc.PLC_VALUE_KEY)
    if not datas:

        return
    values_list = []

    for item in datas:
        values_list.append(PLC_His(**item))

    # 批量插入
    PLC_His.objects.bulk_create(values_list)


def push_redis(datas):
    '''
    把取到的数据发布到redis
    '''
    cache.set(cc.PLC_VALUE_KEY, datas)


def pub_mqtt(topic, datas):
    '''
    把取到的数据发布到消息队列
    '''
    mq_driver = MqttDriver(cc.mqtt_addr, cc.mqtt_port,
                           cc.mqtt_username, cc.mqtt_password)
    mq_driver.connect_mqtt()

    for item in datas:
        item["device_code"] = item["device_code"].code

    result_msg = mq_driver.publish(topic, datas)
