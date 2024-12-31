import logging
import datetime

logger = logging.getLogger(__file__)

SERVICE_STATE_DEFAULT = "configuration error"
SERVICE_STATE_DISABLED = None

SERVICE_INFO_DEFAULT = "error getting information"
SERVICE_INFO_NOT_CONFIGURED = "not configured"
SERVICE_INFO_DEACTIVATED = "deactivated by config or state"
SERVICE_INFO_ERROR_PREFIX = "error getting information: "
SERVICE_INFO_STATE_DISABLED = "disabled"


def _determine_service_state(service_name, service_data):
    logger.info("determining service status for service '{}' with checker {}".format(service_name, service_data['checker_type']))
    service_obj = service_data['checker']
    logger.debug("service_data" + str(service_data))
    service_state = SERVICE_STATE_DEFAULT
    if service_obj:
        try:
            service_state = service_obj.is_active()
        except Exception:
            logger.exception("Error getting state for {}".format(service_name))    
    logger.debug("service '{}' is {}".format(service_name, service_state))
    return service_state


def _determine_service_info(service_name, service_data, service_state):
    service_info = None
    if ('info' in service_data):
        if service_state is False and not service_data['query_info_even_if_offline']:
            service_info = SERVICE_INFO_DEACTIVATED
            logger.debug("don't determine service info.")
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
    return service_info


def check_health(service_data, put_result_into_service_data=True):
    service_name = service_data['service_name']

    service_state = None
    service_info = None
    if service_data['enabled']:
        service_state = _determine_service_state(service_name, service_data)
        service_info = _determine_service_info(service_name, service_data, service_state)
    else:
        logger.info("service '{}' is deactive.".format(service_name))
        service_state = SERVICE_STATE_DISABLED
        service_info = SERVICE_INFO_STATE_DISABLED

    # take the current time
    service_time = datetime.datetime.now().isoformat()

    if put_result_into_service_data:
        service_data['service_state'] = service_state
        service_data['service_info'] = service_info
        service_data['service_time'] = service_time

    return (service_state, service_info, service_time)
