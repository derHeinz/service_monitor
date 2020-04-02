from pydoc import locate

class CompoundExporter(object):

    def create_exporter(self, exporter_config):
        exporter_type = locate(exporter_config['type'])
        return exporter_type(**exporter_config['args'])

    def __init__(self, **kwargs):
        self.exporters_config = kwargs['exporters']
        self.exporters = []
        for exporter_config_name in self.exporters_config:
            exporter_config = self.exporters_config[exporter_config_name]
            self.exporters.append(self.create_exporter(exporter_config))
            
    def export(self, service_info_array):
        for exporter in self.exporters:
            exporter.export(service_info_array)
            