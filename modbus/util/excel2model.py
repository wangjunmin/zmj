
from modbus.models import DeviceInfo, SensorRead


def row2model(item):
    '''
    存储行信息到数据库表
    '''
    if item:
        sensor = SensorRead()
        device_name = item[1]
        try:
            device = DeviceInfo.objects.get(name=device_name)
        except:
            raise Exception("%s:无设备或者有多个设备。" % device_name)
        sensor.device_code = device
        sensor.code = item[2]
        sensor.name = item[3]
        sensor.point_addr = item[4]
        sensor.point_type = item[5]
        sensor.adjust_factor = item[6]
        sensor.data_unit = item[7]
        sensor.demo = item[8]
        sensor.save()
    else:
        raise Exception("需要传递一个测点参数数组,例如：[编号，设备名称，...,数据单位，备注]。")
