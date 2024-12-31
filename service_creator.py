from pydoc import locate
import logging

logger = logging.getLogger(__name__)


def create_service(service_name, service_config):
    logger.debug("reading config of service '{}'".format(service_name))

    service_args = {}
    service_args['service_name'] = service_name

    service_args['service_config'] = service_config

    service_group = service_config['group']
    service_args['service_group'] = service_group

    checker_type = service_config['checker_type']
    service_args['checker_type'] = checker_type
    checker_type_class = locate(checker_type)
    if None is checker_type_class:
        logger.error("Cannot locate checker of type {}".format(checker_type))
    service_args['checker_type_class'] = checker_type_class

    checker_obj = None
    if checker_type_class:
        try:
            checker_obj = checker_type_class(**service_config['checker_args'])
        except Exception:
            logger.exception("Error configuring checker for {}".format(service_name))

    service_args['checker'] = checker_obj

    if 'info_type' in service_config:

        info_type = service_config['info_type']
        service_args['info_type'] = info_type
        info_type_class = locate(info_type)
        if None is info_type_class:
            logger.error("Cannot locate info of type {}".format(info_type))
        service_args['info_type_class'] = info_type_class

        info_obj = None
        if info_type_class:
            try:
                info_obj = info_type_class(**service_config['info_args'])
            except Exception:
                logger.exception("Error configuring info for {}".format(service_name))

        service_args['info'] = info_obj

    # enabled flag for disabling without removal from configuration
    enabled = service_config.get('enabled', True)
    enabled_values_for_false = ["false", "False", False]
    if enabled in enabled_values_for_false:
        enabled = False
    else:
        enabled = True
    service_args['enabled'] = enabled
    if not enabled:
        logger.debug("service '{}' disabled.".format(service_name))

    # flag indicating whether to query info's even if the checker resulted in False
    query = service_config.get('query_info_even_if_offline', False)
    query_values_for_true = ["true", "True", True]
    if query in query_values_for_true:
        query = True
    else:
        query = False
    service_args['query_info_even_if_offline'] = query

    return service_args


def create_services(config):
    services_config = config['services']

    services_list = []
    for service_name in services_config:
        service_args = create_service(service_name, services_config[service_name])
        services_list.append(service_args)

    return services_list
