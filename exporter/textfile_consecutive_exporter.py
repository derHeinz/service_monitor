import time
import logging

logger = logging.getLogger(__file__)

class TextFileConsecutiveExporter(object):

    def __init__(self, **kwargs):
        self.filename = kwargs['filename']
        
    def export(self, service):
        
        service_name = service['service_name']
        service_time = service['service_time']
        service_state = service['service_state']
        service_info = service.get('service_info', "no info available")
        service_state_checker_type = service['checker_type']
        service_info_type = service.get('info_type', "no type available")
        service_exporter_hints = service['service_config'].get('exporter_hints', None)
        
        # write to file
        with open(self.filename, "a") as file_handle:
            # put together the serviec and it's state
            file_handle.write("###\n")
            file_handle.write("service_name: " + str(service_name) + "\n")
            file_handle.write("service_time: " + str(service_time) + "\n")
            file_handle.write("service_state: " + str(service_state)+ "\n")
            file_handle.write("service_info: " + str(service_info) + "\n")
            file_handle.write("###\n")
            time.sleep(10)
    