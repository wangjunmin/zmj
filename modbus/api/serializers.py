from dataclasses import fields
from rest_framework import serializers, viewsets
from modbus.models import DeviceInfo
from modbus.models import SensorRead

class DeviceSerializer(serializers.ModelSerializer):
    '''
    设备序列化
    '''
    class Meta:
        model = DeviceInfo
        fields = '__all__'


class SensorSerializer(serializers.ModelSerializer):
    '''
    测点序列化
    '''
    class Meta:
        model = SensorRead
        fields = '__all__'
