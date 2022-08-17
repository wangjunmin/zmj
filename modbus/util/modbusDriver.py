

import time
from modbus.models import DeviceInfo, SensorRead

import modbus_tk.modbus_tcp as mt
import modbus_tk.defines as md

import sympy


class modbusDriver():
    '''
    modbus 驱动程序
    '''
    master = None

    def __init__(self, device_name):

        self.device_object = DeviceInfo.objects.get(name=device_name)

    def get_driver(self):
        if not self.device_object:
            return None
        self.master = mt.TcpMaster(
            self.device_object.IP_Add, self.device_object.port)
        self.master.set_timeout(self.device_object.time_out)
        self.master.open()

    def get_values(self):
        '''
        从PLC中读取设备中的所有值
        '''

        self.get_driver()
        # 获取测点信息
        sensors = SensorRead.objects.filter(
            device_code=self.device_object).order_by("point_addr")
        point_list, item_dict = self.do_adjust(sensors)

        result_list = []
        if not self.master:
            raise Exception("与PLC连接失败，请检查设备配置项")

        for points in point_list:
            data_value = self.get_sensor_value(points)

            result_list.extend(self.fill_data(item_dict, data_value, points))
        self.master.close()
        return result_list

    def get_sensor_value(self, points):
        '''
        从PLC中获取值
        '''
        data_sam = self.master.execute(
            slave=self.device_object.slave,
            function_code=md.READ_HOLDING_REGISTERS,
            starting_address=points[0],
            quantity_of_x=len(points))
        return data_sam

    def fill_data(self, sensor_dict, data_value, points):
        '''
        装配数据，数据格式为json
        '''
        result_list = []

        for index, point in enumerate(points):
            result = {}
            sensors = sensor_dict[point]
            for sensor in sensors:
                # 设备代码
                result["device_code"] = sensor.device_code
                # 设备名称
                result["device_name"] = self.device_object.name
                # 测点代码
                result["sensor_code"] = sensor.code
                # 测点名称
                result["sensor_name"] = sensor.name
                # 测点值
                result["sensor_value"] = data_value[index]
                result['adjust_value'] = self.adjust_value(data_value[index],
                                                           sensor.adjust_factor, sensor.point_type)
                # 测点单位
                result["sensor_unit"] = sensor.data_unit
                # 数据时间
                result["data_time"] = time.time()
                result_list.append(result)
        return result_list

    def adjust_value(self, value, adjust_factor, data_type):
        '''
        获取值的调整因子，支持各种代数式，变量为‘x’
        '''

        if data_type == 'short' or data_type == 'float':
            if adjust_factor:
                try:
                    x = sympy.Symbol("x")
                    expr_func = sympy.lambdify(x, adjust_factor)
                    return expr_func(value)
                except Exception as e:
                    return None
            else:
                return value

        elif data_type.startswith('bit'):

            return self.pros_bit(value, data_type)
        else:
            return value

    def pros_bit(self, value, data_type):
        '''
        计算位取数的内容。
        '''
        numbers = [int(temp)
                   for temp in list(data_type) if temp.isdigit()]
        if len(numbers) == 0:
            return value
        bit_num = numbers[0]

        bin_str = bin(int(value)).replace('0b', '')
        if len(bin_str) < bit_num:
            return 0
        else:
            return bin_str[-bit_num-1]

    def do_adjust(self, sensers):
        '''
        把传感器按照连续的位置分成段，每段最多只能有100个
        返回分段的位置列表， 该分段对应的传感器
        '''
        item_list = {}
        for senser in sensers:
            key1 = senser.point_addr

            if item_list.get(key1):
                s_list = item_list.get(key1)
                s_list.append(senser)
                item_list[key1] = s_list
            else:
                s_list = [senser]
                item_list[key1] = s_list

        keys = list(item_list .keys())
        start, end = keys[0], keys[-1]
        sub_point_list = []
        point_list = []
        for counter in range(start, end+1):
            if counter in keys:
                if len(sub_point_list) >= 80 or counter == end:
                    point_list.append(sub_point_list)
                    sub_point_list = []
                sub_point_list.append(counter)

            else:
                if len(sub_point_list) > 0:
                    point_list.append(sub_point_list)
                sub_point_list = []

        return point_list, item_list
