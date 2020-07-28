from pydoc import locate

class CompoundExporter(object):

    def create_exporter(self, exporter_config):
        exporter_type = locate(exporter_config['type'])
        return exporter_type(**exporter_config['args'])

    def __init__(self, **kwargs):
        self.exporters_config = kwargs['exporters']
        self.exporters = []
        for single_exporter_config in self.exporters_config:
            self.exporters.append(self.create_exporter(single_exporter_config))
            
    def export(self, element):
        for exporter in self.exporters:
            try:
                exporter.export(element)
            except Exception as e:
                logger.exception("Error exporting '{}' into exporter '{}'".format(element, exporter))
            