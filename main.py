import os
import logging
from logging.handlers import RotatingFileHandler
from pydoc import locate

from config_helper import load_config_file

class Service(object):
    
    def __init__(self, **kwargs):
        self.checker_obj = kwargs['checker_obj']
        self.info_obj = kwargs.get('info_obj', None)
        self.enabled = kwargs['enabled']
        

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

def create_services(config):
    services_config = config['services']

    services_list = []
    for service_name in services_config:
        logging.debug("reading config of service '{}'".format(service_name))
        
        service_args = {}
        service_args['service_name'] = service_name
        
        service_config = services_config[service_name]
        service_args['service_config'] = service_config
        
        service_group = service_config['group']
        service_args['service_group'] = service_group
        
        checker_type = locate(service_config['checker_type'])
        service_args['checker_type'] = checker_type
        
        checker_obj = checker_type(**service_config['checker_args'])
        service_args['checker'] = checker_obj

        if 'info_type' in service_config:
            info_type = locate(service_config['info_type'])
            service_args['info_type'] = info_type
            info_obj = info_type(**service_config['info_args'])
            service_args['info'] = info_obj
        
        # enabled flag for disabling without removal from configuration
        enabled =  service_args.get('enabled', True)
        service_args['enabled'] = enabled
        if not enabled:
            logging.debug("service '{}' disabled.".format(service_name))
            
        # flag indicating whether to query info's even if the checker resulted in False
        query = service_args.get('query_info_even_if_offline', False)
        service_args['query_info_even_if_offline'] = query
        
        services_list.append(service_args)

    return services_list
    
def create_exporter(config):
    exporter_config = config['exporter']
    exporter_type = locate(exporter_config['type'])
    return exporter_type(**exporter_config['args'])
    
def check_health(services_list):
    for service in services_list:
        service_name = service['service_name']
        logging.debug("determining service status for service '{}' with checker {}".format(service_name, service['checker_type']))
        service_obj = service['checker']
        service_state = service_obj.is_active()
        service['service_state'] = service_state
        logging.debug("service '{}' is {}".format(service_name, service_state))
        
        if 'info' in service:
            if service_state or service['query_info_even_if_offline']:
                logging.debug("determining information for service '{}' with infos {}".format(service_name, service['info_type']))
                info_obj = service['info']
                service_info = info_obj.query_info()
                logging.debug("service '{}' has info {}".format(service_name, service_info))
                service['service_info'] = service_info

def main():
    setup_logging()
    config = load_config_file('config.json')
    logging.debug("config: {}".format(config))
    services_list = create_services(config)
    check_health(services_list)
    
    exporter = create_exporter(config)
    exporter.export(services_list)

# Main function
if __name__ == "__main__":
    main()