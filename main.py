import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pydoc import locate

from config_helper import load_config_file
from service_creator import create_services
from health_checker import check_health_for_services

logger = logging.getLogger(__file__)

def setup_logging():
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    #file_handler = RotatingFileHandler("/tmp/service_monitor.log", maxBytes=153600, backupCount=3)
    #file_handler.setLevel(logging.DEBUG)
    #file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)
    #root_logger.addHandler(file_handler)

def create_exporter(config):
    exporter_config = config['exporter']
    exporter_type = locate(exporter_config['type'])
    return exporter_type(**exporter_config['args'])
    
def main():
    setup_logging()
    config = load_config_file('config.json')
    logger.debug("config: {}".format(config))
    services_list = create_services(config)
    check_health_for_services(services_list)
    
    exporter = create_exporter(config)
    exporter.export(services_list)

# Main function
if __name__ == "__main__":
    main()