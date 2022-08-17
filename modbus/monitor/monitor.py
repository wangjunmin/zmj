
import logging
from django.core.cache import cache

from modbus.modbus_config import Constant_config


def doMonitor():
    '''
    监控系统健康状况。
    包括系统数据采集情况统计、系统心跳情况查询等内容。
    '''
    device_info = {
        "status": get_device_status(),
        "col_count": Constant_config.col_count,
        "err_count": Constant_config.err_count,
        "col_interval_time": Constant_config.col_interval_time
    }
    return device_info


def doExcept(key, err):
    '''
    处理出错。
    保留出错多少次后，连续出错10次后，系统降低采集频率的需求实现。
    '''
    Constant_config.device_status = False
    Constant_config.err_count += 1

    logging.info(key, err)
    # 先判断该key是否存在
    if cache.ttl(key):
        # 存在，并设置了过期时间
        counter = cache.get(key)
        if counter > 10:
            # 超过10次出错，需要降低采集频率，计数器重置
            slow_freq()
            # 删除重置
            cache.set(key, 1)
        else:
            cache.set(key, counter+1)
    else:
        cache.set(key, 1, 300*60)


def slow_freq():
    '''
    降低采集频率
    '''
    pass


def doNormal(key):
    '''
    连续采集3次后，恢复正常的频率
    '''
    Constant_config.device_status = True
    Constant_config.col_count += 1
    # 清除错误的key
    cache.delete(Constant_config.PLC_ERR)


def get_device_status():
    return Constant_config.device_status
