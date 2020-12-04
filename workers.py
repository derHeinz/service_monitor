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

class ConsecutiveWorker(object):

    class JobExecutor(object):
        
        def __init__(self, exporter):
            self.exporter = exporter
            
        def execute(self, service):
            res = _health_check_and_result(service)
            self.exporter.export(service)

    def __init__(self, services_list, exporter, **kwargs):
        self.exporter = exporter
        self.services_list = services_list
        self.job_executor = self.JobExecutor(exporter)
        
        # if the exporter is able to callback
        set_worker_callback = getattr(self.exporter, "set_worker_callback", None)
        if set_worker_callback:
            if callable(set_worker_callback):
                logger.debug("found callback in exporter {}".format(str(type(self.exporter))))
                set_worker_callback(self.work_single)

    def work_single(self, service_name):
        logger.debug("requesting an out-of-order processing for service: {}".format(service_name))
        for service in self.services_list:
            #find the one with 'service_name' == service_name
            if service['service_name'] == service_name:
                self.job_executor.execute(service)
                break
        
        

    def work_all(self, workers):
    
        if workers:
            logger.debug("running with {} workers".format(workers))
            pool = Pool(processes=workers)
            while True:
                start_time = time.time()
                pool.map(self.job_executor.execute, self.services_list)
                end_time = time.time()
                logger.debug("needed {}s to process a full cycle".format((end_time - start_time)))
            
        else:
            logger.debug("running without workers")
            while True:
                start_time = time.time()
                for service in self.services_list:
                    self.job_executor.execute(service)
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

    def __init__(self, services_list, exporter, **kwargs):
        self.exporter = exporter
        self.services_list = services_list
    
    def work_all(self, workers):
    
        # calculate health
        results = None
        
        start_time = time.time()
        if workers:
            logger.debug("running with {} workers".format(workers))
            procs = workers
            p = Pool(processes=procs)
            results = p.map(_as_job, self.services_list)
        else:
            logger.debug("running without workers")
            for service in self.services_list:
                _health_check_and_result(service)
            results = self.services_list
        end_time = time.time()
        logger.debug("needed {}s to process".format((end_time - start_time)))
        
        self.exporter.export(results)
        # wait a little
        time.sleep(2)
        os._exit(0)
