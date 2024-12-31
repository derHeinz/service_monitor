#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import logging

logger = logging.getLogger(__file__)


def read_config_file(filename):
    logger.info("reading file {}".format(filename))
    relative_path = os.path.join(os.path.dirname(__file__), filename)
    with open(relative_path) as data_file:
        return json.load(data_file)


def load_config_file(filename):

    data = read_config_file(filename)
    # load subconfig files
    subconfigfiles = data.get("configfiles")
    if subconfigfiles:
        logger.debug("loading subconfigs")
        for subconfigfile in subconfigfiles:

            subconfig_data = read_config_file(subconfigfile)
            # merge into data
            services_data = data.get('services')
            if services_data:
                # check for duplicates
                for service_name in services_data:
                    if service_name in subconfig_data:
                        services_data[service_name] = None
                        logger.error("Duplicate service definition for {service} in file {file}. Using config of {file}.".format(service=service_name, file=subconfigfile))
                services_data.update(subconfig_data)
            else:
                data['services'] = subconfig_data  

    logger.debug(json.dumps(data, indent=4, sort_keys=True))
    return data
