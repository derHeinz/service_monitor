import os
import logging
from logging.handlers import RotatingFileHandler
from pydoc import locate

from config_helper import load_config_file

def setup_logging():
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    
    #file_handler = RotatingFileHandler("/tmp/service_monitor.log", maxBytes=153600, backupCount=3)
    #file_handler.setLevel(logging.DEBUG)
    #file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)
    #root_logger.addHandler(file_handler)

def create_servicedict(config):
    services_config = config['services']

    servicename_to_serviceobject = {}
    for service_name in services_config:
        logging.debug("reading config of service '{}'".format(service_name))
        service_data_config = services_config[service_name]
        
        service_type = locate(service_data_config['type'])
        service_obj = service_type(**service_data_config['args'])
        
        enabled = True
        if 'enabled' in service_data_config:
            if not service_data_config['enabled']:
                logging.debug("service '{}' disabled.".format(service_name))
                enabled = False
        if enabled:
            servicename_to_serviceobject.update({service_name: service_obj})

    return servicename_to_serviceobject
    
def create_exporter(config):
    exporter_config = config['exporter']
    exporter_type = locate(exporter_config['type'])
    return exporter_type(**exporter_config['args'])
    
def check_health(services_dict):
    service_names = []
    service_states = []
    for service_name, service_obj in services_dict.items():
        logging.debug("determining service status for service '{}' with checker {}".format(service_name, service_obj))
        service_state = service_obj.is_active()
        logging.debug("service '{}' is {}".format(service_name, service_state))
        service_names.append(service_name)
        service_states.append(service_state)
    return service_names, service_states

def main():
    setup_logging()
    config = load_config_file('config.json')
    logging.debug("config: {}".format(config))
    service_dict = create_servicedict(config)
    exporter = create_exporter(config)

    service_names, service_states = check_health(service_dict)
    exporter.export(service_names, service_states)

# Main function
if __name__ == "__main__":
    main()