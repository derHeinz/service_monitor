import argparse
import logging
import time
import os
import signal
from logging.handlers import RotatingFileHandler
from pydoc import locate

from workers import OnceWorker, ConsecutiveWorker
from config_helper import load_config_file
from service_creator import create_services

logger = logging.getLogger(__file__)

def exit_program(signal, frame):
    time.sleep(2)
    os._exit(0)

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

def create_exporter(config, exporter_config_name):
    exporter_config = config[exporter_config_name]
    exporter_type = locate(exporter_config['type'])
    return exporter_type(**exporter_config['args'])

def main():
    parser = argparse.ArgumentParser(description="service_monitor command line interface.")
    parser.add_argument("-c", dest="config", type=str, metavar="config", nargs="?", help="Optional config file name/location.")
    args = parser.parse_args()
    
    config_file = args.config if args.config else 'config.json'
    
    signal.signal(signal.SIGINT, exit_program)
    setup_logging()
    logger.debug("loading from config file {}", config_file)
    config = load_config_file(config_file)
    logger.debug("config: {}".format(config))
    
    # parse things todo
    services_list = create_services(config)
    number_of_workers = config.get('workers', None)
    
    consecutive = config.get('consecutive', False)

    worker = None
    exporter = None
    if consecutive:
        logger.info("working repeatedly on all services.")
        exporter = create_exporter(config, 'exporter_consecutive')
        worker = ConsecutiveWorker()
    else:
        logger.info("working once on all services.")
        exporter = create_exporter(config, 'exporter')
        worker = OnceWorker()
    worker.work(services_list, number_of_workers, exporter)
    

# Main function
if __name__ == "__main__":
    main()
