
from ctypes.wintypes import PLCID


class Constant_config:
    '''
    应用的常量
    '''
    PLC_ERR = "PLC_ERR"

    PLC_NORMAL = 'PLC_NORMAL'

    PLC_VALUE_KEY = "PLC_VALUE"

    INI_INTERVAL = 2

    COL_INTERVAL = INI_INTERVAL
    MAX_INTERVAL = 1800
    device_status = True

    col_count = 0
    err_count = 0
    col_interval_time = 0
    err_message = ""
    # 设备列表的定义
    device_list = []

    mqtt_addr = "127.0.0.1"
    mqtt_port = 1883
    mqtt_username = "admin"
    mqtt_password = "public"
    # 判断是否写入历史库。
    switch_his = False
