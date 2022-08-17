
from paho.mqtt import client as mqtt_client
import random
import json


class MqttDriver():
    client = None

    def __init__(self, broker, port, username, password) -> None:
        self.broker = broker
        self.port = port
        self.client_id = str(random.randint(1, 100000))
        self.username = username
        self.password = password

    def connect_mqtt(self):
        if MqttDriver.client:
            return
        else:
            MqttDriver.client = mqtt_client.Client(self.client_id)
            MqttDriver.client.username_pw_set(self.username, self.password)
            MqttDriver.client.connect(self.broker, self.port)
            MqttDriver.client.loop_start()

    def publish(self, topic, msg):

        result = MqttDriver.client.publish(topic, json.dumps(msg))
        return result

    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    def get_client(self):
        return MqttDriver.client
