import logging

logger = logging.getLogger(__file__)

SERVICE_STATE_DEFAULT = "configuration error"

SERVICE_INFO_DEFAULT = "error getting information"
SERVICE_INFO_NOT_CONFIGURED = "not configured"
SERVICE_INFO_DEACTIVATED = "deactivated by config or state"
SERVICE_INFO_ERROR_PREFIX = "error getting information: "

def check_health(service_data, put_result_into_service_data=True):
    service_name = service_data['service_name']
    logger.info("determining service status for service '{}' with checker {}".format(service_name, service_data['checker_type']))
    service_obj = service_data['checker']
        
    service_state = SERVICE_STATE_DEFAULT
    if service_obj:
        try:
            service_state = service_obj.is_active()
        except:
            logger.exception("Error getting state for {}".format(service_name))    
    logger.debug("service '{}' is {}".format(service_name, service_state))

    service_info = None
    if ('info' in service_data):
        if service_state==False and not service_data.get('query_info_even_if_offline', False):
            service_info = SERVICE_INFO_DEACTIVATED
        else:
            logger.info("determining information for service '{}' with infos {}".format(service_name, service_data['info_type']))
            info_obj = service_data['info']
            service_info = SERVICE_INFO_DEFAULT
            if info_obj:
                try:
                    service_info = info_obj.query_info()
                except Exception as e:
                    service_info = SERVICE_INFO_ERROR_PREFIX + str(e)
                    logger.exception("Error getting info for {}".format(service_name)) 
            logger.debug("service '{}' has info {}".format(service_name, service_info))
    else:
        service_info = SERVICE_INFO_NOT_CONFIGURED
        
    if put_result_into_service_data:
        service_data['service_state'] = service_state
        service_data['service_info'] = service_info
        
    return (service_state, service_info)

def check_health_for_services(services_list):
    for service in services_list:
        check_health(service)