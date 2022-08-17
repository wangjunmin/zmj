
from django.db import models
from pkg_resources import require

# Create your models here.


class DeviceInfo(models.Model):
    '''
    设备信息，包括设备的连接信息。
    '''
    code = models.CharField(
        verbose_name="编码", max_length=30, primary_key=True
    )
    name = models.CharField(verbose_name="名称", max_length=50)
    proxy = models.CharField(
        verbose_name="协议", max_length=10, default="Modbus")
    IP_Add = models.CharField(verbose_name="IP地址", max_length=30)
    port = models.IntegerField(verbose_name="端口号", default=502)
    slave = models.IntegerField(verbose_name="从站编号", default=1)
    mode = models.CharField(verbose_name="模式", choices=[(
        "RTU", "RTU"), ("ASCII", "ASCII")], max_length=8)
    time_out = models.IntegerField(verbose_name="超时设置", default=2000)
    time_interval = models.IntegerField(verbose_name='采集周期（秒）', default=20)
    demo = models.CharField(verbose_name="备注", max_length=100,
                            default=None, null=True, blank=True)
    device_desc = models.CharField(
        verbose_name="设备描述", max_length=200, null=True, blank=True, default=None)


class SensorRead(models.Model):
    """
    记录测点信息,只读的测点信息配置
    """

    device_code = models.ForeignKey(DeviceInfo, on_delete=models.DO_NOTHING)
    code = models.CharField(verbose_name="代码", max_length=30)
    name = models.CharField(verbose_name="测点名称", max_length=30)
    point_addr = models.IntegerField(verbose_name="测点地址")
    point_type = models.CharField(verbose_name="数据类型", max_length=64, choices=[
                                  ("float", "float"), ("bool", "bool"), ("string", "string")])
    # 目前只支持 线性调整
    adjust_factor = models.CharField(
        verbose_name="调整因子", max_length=100, default=None, null=True, blank=True)
    data_unit = models.CharField(
        verbose_name="数据单位", default=None, max_length=30, blank=True, null=True)
    demo = models.CharField(verbose_name="备注", max_length=200,
                            default=None, null=True, blank=True)


class PLC_His(models.Model):
    '''
    数据采集的历史值
    '''
    device_code = models.CharField(verbose_name="设备编码", max_length=30)
    device_name = models.CharField(verbose_name="设备名称", max_length=50)
    sensor_code = models.CharField(verbose_name="测点编码", max_length=30)
    sensor_name = models.CharField(verbose_name="测点名称", max_length=50)
    sensor_value = models.CharField(verbose_name="测点原始值", max_length=64)
    adjust_value = models.CharField(verbose_name="测点计算值", max_length=64)
    sensor_unit = models.CharField(
        verbose_name="测点单位", max_length=10, default=None, null=True, blank=True)
    data_time = models.DateTimeField(
        verbose_name="数据时间", auto_now=True, primary_key=True)


class Err_Info(models.Model):
    '''
    出错信息日志
    '''
    device_name = models.CharField(verbose_name="设备名称", max_length=50)
    data_time = models.DateTimeField(
        verbose_name="数据时间", auto_now=True, primary_key=True)
    err_info = models.CharField(verbose_name="出错信息", max_length=300,
                                default=None, blank=True, null=True)
    err_count = models.IntegerField(
        verbose_name="连续次数", default=None, blank=True, null=True
    )


class sys_config(models.Model):
    '''
    记录系统的配置信息，初始化。
    '''
    name = models.CharField(verbose_name="配置名称", max_length=30, default=None)
    code = models.CharField(verbose_name="配置代码", max_length=20,
                            help_text="需要与说明书中的代码保持一致", primary_key=True)
    value = models.CharField(
        verbose_name="配置值", max_length=100, help_text="如果为开关量：0表示False，1表示True")
    desc = models.CharField(verbose_name="备注", max_length=100,
                            blank=True, default=None, null=True)

    class Meta:
        verbose_name = "系统配置表"
        verbose_name_plural = "系统配置表"
