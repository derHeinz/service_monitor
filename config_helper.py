#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

def load_config_file(filename):
    
    relative_path = os.path.join(os.path.dirname(__file__), filename)
    with open(relative_path) as data_file:    
        data = json.load(data_file)
        return data