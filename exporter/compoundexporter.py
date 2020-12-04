from pydoc import locate
import logging

logger = logging.getLogger(__file__)

class CompoundExporter(object):

    def create_exporter(self, exporter_config):
        exporter_type = locate(exporter_config['type'])
        return exporter_type(**exporter_config['args'])

    def __init__(self, **kwargs):
        self.exporters_config = kwargs['exporters']
        self.exporters = []
        self.service_callback = None
        
        for single_exporter_config in self.exporters_config:
            self.exporters.append(self.create_exporter(single_exporter_config))
            
    def export(self, element):
        for exporter in self.exporters:
            try:
                exporter.export(element)
            except Exception as e:
                logger.exception("Error exporting '{}' into exporter '{}'".format(element, exporter))
            
    def set_worker_callback(self, service_worker_callback):
        for exporter in self.exporters:
            callback = getattr(exporter, "set_worker_callback", None)
            if callback:
                if callable(callback):
                    logger.debug("found callback in exporter {}".format(str(type(exporter))))
                    callback(service_worker_callback)