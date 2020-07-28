import logging
import os
import time
from multiprocessing import Pool
from health_checker import check_health_for_services, check_health

logger = logging.getLogger(__file__)

class JobExecutor(object):
    
    def __init__(self, exporter):
        self.exporter = exporter
        
    def execute(self, service):
        res = check_health(service)
        service['service_state'] = res[0]
        service['service_info'] = res[1]
        service['service_time'] = res[2]
        self.exporter.export(service)

class ConsecutiveWorker(object):

    def work(self, services_list, workers, exporter):
    
        je = JobExecutor(exporter)
        if workers:
            logger.debug("running with {} workers".format(workers))
            pool = Pool(processes=workers)
            while True:
                start_time = time.time()
                pool.map(je.execute, services_list)
                end_time = time.time()
                logger.debug("needed {}s to process a full cycle".format((end_time - start_time)))
            
        else:
            logger.debug("running without workers")
            while True:
                start_time = time.time()
                for service in services_list:
                    je.execute(service)
                end_time = time.time()
                logger.debug("needed {}s to process a full cycle".format((end_time - start_time)))
            
        # will never come...

def as_job(service_data):
    res = check_health(service_data)
    service_data['service_state'] = res[0]
    service_data['service_info'] = res[1]
    service_data['service_time'] = res[2]
    return service_data

class OnceWorker(object):
    
    def work(self, services_list, workers, exporter):
    
        # calculate health
        results = None
        
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
