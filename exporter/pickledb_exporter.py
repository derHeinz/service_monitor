import logging
import pickledb 

logger = logging.getLogger(__file__)

class PickleDBExporter(object):

    def __init__(self, **kwargs):
        self.db_file = kwargs.get("db_file", "service_monitor.db")
        self.export_config = kwargs.get("export_config", False)
        self.db = pickledb.load(self.db_file, False) 
            
    def export(self, element):
        service_name = element['service_name']
        keys_to_export = ['service_state', 'service_info', 'service_time']
        if self.export_config:
            keys_to_export.append('service_config')
        exportable = { key: element[key] for key in keys_to_export }
        
        if not service_name in self.db.getall():
            self.db.lcreate(service_name)
        self.db.ladd(service_name, exportable)
        self.db.dump()

    def set_worker_callback(self, service_worker_callback):
        pass
