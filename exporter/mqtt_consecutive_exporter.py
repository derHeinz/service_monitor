
import logging
import json
import paho.mqtt.client as mqtt

logger = logging.getLogger(__file__)

class MqttConsecutiveExporter(object):

    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.port = int(kwargs.get('port', 1883))
        self.topic = kwargs.get('topic', 'service_monitor')
        
        self.client = mqtt.Client()
        self.client.connect(self.host, self.port, 60)
        self.client.on_connect = self._on_connect
        
    def _on_connect(self):
        logger.debug("connected to mqtt")
        
    def export(self, service):
        keys_to_export = ['service_name', 'service_config', 'service_state', 'service_info', 'service_time']
        exportable = { key: service[key] for key in keys_to_export }
        service_name = service['service_name']
        json_string = json.dumps(exportable)
        self.client.publish(self.topic + "/" + service_name, json_string)
