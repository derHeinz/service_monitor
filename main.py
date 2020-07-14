import logging
import time
import os
from logging.handlers import RotatingFileHandler
from pydoc import locate
from multiprocessing import Pool

from config_helper import load_config_file
from service_creator import create_services
from health_checker import check_health_for_services, check_health

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
    
def as_job(service_data):
    res = check_health(service_data)
    service_data['service_state'] = res[0]
    service_data['service_info'] = res[1]
    return service_data
    
def main():
    setup_logging()
    config = load_config_file('config.json')
    logger.debug("config: {}".format(config))
    
    services_list = create_services(config)
    exporter = create_exporter(config)
    
    # calculate health
    results = None
    workers = config.get('workers', None)
    start_time = time.time()
    if workers:
        logger.debug("running with {} workers".format(workers))
        procs = workers
        p = Pool(processes=procs)
        results = p.map(as_job, services_list)
    else:
        logger.debug("running without workers")
        check_health_for_services(services_list)
        results = services_list
    end_time = time.time()
    logger.debug("needed {}s to process".format((end_time - start_time)))
    
    exporter.export(results)
    # wait a little
    time.sleep(2)
    os._exit(0)

# Main function
if __name__ == "__main__":
    main()