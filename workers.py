import logging
import os
import time
import health_checker
from multiprocessing import Pool

logger = logging.getLogger(__file__)

def _health_check_and_result(service):
    res = health_checker.check_health(service)
    service['service_state'] = res[0]
    service['service_info'] = res[1]
    service['service_time'] = res[2]
    return res

class JobExecutor(object):
    
    def __init__(self, exporter):
        self.exporter = exporter
        
    def execute(self, service):
        res = _health_check_and_result(service)
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
                sleep_time = 60*5
                logger.info("now waiting {}s for the next cycle.".format(sleep_time))
                time.sleep(sleep_time)
            
        # will never come...

def _as_job(service_data):
    res = _health_check_and_result(service_data)
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
            results = p.map(_as_job, services_list)
        else:
            logger.debug("running without workers")
            for service in services_list:
                _health_check_and_result(service)
            results = services_list
        end_time = time.time()
        logger.debug("needed {}s to process".format((end_time - start_time)))
        
        exporter.export(results)
        # wait a little
        time.sleep(2)
        os._exit(0)
