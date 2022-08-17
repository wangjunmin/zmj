# Generated by Django 3.2.13 on 2022-08-11 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceInfo',
            fields=[
                ('code', models.CharField(max_length=30, primary_key=True, serialize=False, verbose_name='编码')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('proxy', models.CharField(default='Modbus', max_length=10, verbose_name='协议')),
                ('IP_Add', models.CharField(max_length=30, verbose_name='IP地址')),
                ('port', models.IntegerField(default=502, verbose_name='端口号')),
                ('slave', models.IntegerField(default=1, verbose_name='从站编号')),
                ('mode', models.CharField(choices=[('RTU', 'RTU'), ('ASCII', 'ASCII')], max_length=8, verbose_name='模式')),
                ('time_out', models.IntegerField(default=2000, verbose_name='超时设置')),
                ('time_interval', models.IntegerField(default=20, verbose_name='采集周期（秒）')),
                ('demo', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='备注')),
                ('device_desc', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='设备描述')),
            ],
        ),
        migrations.CreateModel(
            name='Err_Info',
            fields=[
                ('device_name', models.CharField(max_length=50, verbose_name='设备名称')),
                ('data_time', models.DateTimeField(auto_now=True, primary_key=True, serialize=False, verbose_name='数据时间')),
                ('err_info', models.CharField(blank=True, default=None, max_length=300, null=True, verbose_name='出错信息')),
                ('err_count', models.IntegerField(blank=True, default=None, null=True, verbose_name='出错次数')),
            ],
        ),
        migrations.CreateModel(
            name='PLC_His',
            fields=[
                ('device_code', models.CharField(max_length=30, verbose_name='设备编码')),
                ('device_name', models.CharField(max_length=50, verbose_name='设备名称')),
                ('sensor_code', models.CharField(max_length=30, verbose_name='测点编码')),
                ('sensor_name', models.CharField(max_length=50, verbose_name='测点名称')),
                ('sensor_value', models.CharField(max_length=64, verbose_name='测点原始值')),
                ('adjust_value', models.CharField(max_length=64, verbose_name='测点计算值')),
                ('sensor_unit', models.CharField(blank=True, default=None, max_length=10, null=True, verbose_name='测点单位')),
                ('data_time', models.DateTimeField(auto_now=True, primary_key=True, serialize=False, verbose_name='数据时间')),
            ],
        ),
        migrations.CreateModel(
            name='SensorRead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30, verbose_name='代码')),
                ('name', models.CharField(max_length=30, verbose_name='测点名称')),
                ('point_addr', models.IntegerField(verbose_name='测点地址')),
                ('point_type', models.CharField(choices=[('float', 'float'), ('bool', 'bool'), ('string', 'string')], max_length=64, verbose_name='数据类型')),
                ('adjust_factor', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='调整因子')),
                ('data_unit', models.CharField(blank=True, default=None, max_length=30, null=True, verbose_name='数据单位')),
                ('demo', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='备注')),
                ('device_code', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='modbus.deviceinfo')),
            ],
        ),
    ]
