import logging
from pydoc import locate

logger = logging.getLogger(__file__)

SERVICE_INFO_ERROR_PREFIX = "error getting information: "


class CompoundInfo(object):

    def create_info(self, info_config):
        info_type = locate(info_config['info_type'])
        return info_type(**info_config['info_args'])

    def __init__(self, **kwargs):
        self.infos_config = kwargs['infos']
        self.infos = []
        for single_info_config in self.infos_config:
            self.infos.append(self.create_info(single_info_config))

    def query_info(self):

        query_info_result = []

        for info in self.infos:
            service_info = None
            try:
                service_info = info.query_info()
            except Exception as e:
                service_info = SERVICE_INFO_ERROR_PREFIX + str(e)
                logger.exception("Error getting info for {}".format(info))
            query_info_result.append(service_info)
            logger.debug("infoer '{}' has infos: {}".format(info, service_info))

        return query_info_result
