
import logging
from datetime import datetime
import dateutil.parser
from pytz import timezone
from influxdb import InfluxDBClient
from tzlocal import get_localzone # $ pip install tzlocal

logger = logging.getLogger(__file__)

def bool_to_1_or_0(b):
    if (b):
        return 1
    else:
        return 0

class InfluxDBConsecutiveExporter(object):

    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.port = int(kwargs.get('port', 8086))
        self.dbname = kwargs.get('dbname', 'service_monitor')
        self.username = kwargs.get('user', None)
        self.password = kwargs.get('password', None)
        
        self.client = InfluxDBClient(self.host, self.port, self.username, self.password, self.dbname)
        
    def _on_connect(self):
        logger.debug("connected to mqtt")
        
    
        
    def export(self, service):
 
        # this is how you convert a datetime to "influx" time
        time_in_iso_localtz = dateutil.parser.isoparse(service['service_time']) # this is in local timezone!
        time_in_iso = time_in_iso_localtz.astimezone(timezone('UTC')) #into UTC
        service_time_for_influx = time_in_iso.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        json_body = [
        {
            "measurement": "allservices",
            "time": service_time_for_influx,
            "tags": {
                "service_name": service['service_name'],
                "service_group": service['service_group'],
                "enabled": bool_to_1_or_0(service['enabled'])
            },
            "fields": {
                "state": bool_to_1_or_0(service['service_state']),
                "info": str(service['service_info'])
            }
        }
        ]
        logger.info("exporting to influx: " + str(json_body))
        
        self.client.write_points(json_body)
