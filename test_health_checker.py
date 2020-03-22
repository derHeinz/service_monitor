import unittest
import json

from health_checker import check_health, SERVICE_INFO_NOT_CONFIGURED, SERVICE_STATE_DEFAULT, SERVICE_INFO_ERROR_PREFIX, SERVICE_INFO_DEACTIVATED

class TrueChecker(object):
    def is_active(self):
        return True
        
class FalseChecker(object):
    def is_active(self):
        return False
        
class ExceptionChecker(object):
    def is_active(self):
        raise ValueError("some error")
        
class SimpleInfo(object):
    def query_info(self):
        return "Test"

class ExceptionInfo(object):
    def query_info(self):
        raise ValueError("some error")

'''
Tests
# check health online(True), offline(False) and error
# check info
# query_info_even_if_offline, not present and set to true
'''

class Testhealth_checker(unittest.TestCase):

    def test_checker(self):
   
        cfg = {'service_name': 'test', 'checker_type': 'Test', 'checker': TrueChecker()}
        self.assertEqual((True, SERVICE_INFO_NOT_CONFIGURED), check_health(cfg))
        
        cfg = {'service_name': 'test', 'checker_type': 'Test', 'checker': FalseChecker()}
        self.assertEqual((False, SERVICE_INFO_NOT_CONFIGURED), check_health(cfg))
        
        # check when checker throws exception
        cfg = {'service_name': 'test', 'checker_type': 'Test', 'checker': ExceptionChecker()}
        self.assertEqual((SERVICE_STATE_DEFAULT, SERVICE_INFO_NOT_CONFIGURED), check_health(cfg))
        
    def test_info_checker(self):
    
        cfg = {'service_name': 'test', 'checker_type': 'Test', 'checker': TrueChecker(),
        'info_type': 'Test', 'info':  SimpleInfo()}
        self.assertEqual((True, "Test"), check_health(cfg))
        
        # check with info throws exception
        cfg = {'service_name': 'test', 'checker_type': 'Test', 'checker': TrueChecker(),
        'info_type': 'Test', 'info':  ExceptionInfo()}
        res = check_health(cfg)
        self.assertTrue(res[0])
        self.assertTrue(res[1].startswith(SERVICE_INFO_ERROR_PREFIX))
        
        
    def test_info_checker_query_info_even_if_offline(self):
    
        # don't check when result is False
        cfg = {'service_name': 'test', 'checker_type': 'Test', 'checker': FalseChecker(),
        'info_type': 'Test', 'info':  SimpleInfo()}
        self.assertEqual((False, SERVICE_INFO_DEACTIVATED), check_health(cfg))
        
        # do check when extra flag is True
        cfg = {'service_name': 'test', 'checker_type': 'Test', 'checker': FalseChecker(),
        'info_type': 'Test', 'info':  SimpleInfo(), 'query_info_even_if_offline': True}
        self.assertEqual((False, "Test"), check_health(cfg))
        
        