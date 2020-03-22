import unittest
import json

from service_creator import create_service

'''
Tests:
# put Groups together
# query_info_even_if_offline

# with or without info

# checker
## illegal class, class not found
## no args, illegal args

# info
## illegal class, class not found
## no args, illegal args
'''

class Testservice_creator(unittest.TestCase):

    def test_create_service_simple(self):
        cfg = '''
        {	
			"group": "Simple Services",
			"checker_type": "checkers.testchecker.TestChecker",
			"checker_args": {
				"return_value": true
			}
		}
        '''
        res = create_service('fake dir', json.loads(cfg))
        self.assertEqual('fake dir', res['service_name'])
        self.assertEqual('Simple Services', res['service_group'])
        self.assertEqual('checkers.testchecker.TestChecker', res['checker_type'])
        
        # defines a type
        self.assertEqual('type', type(res['checker_type_class']).__name__)
        self.assertEqual('TestChecker', type(res['checker']).__name__)
        
    def test_create_service_error(self):
        # illegal class
        cfg = '''
        {	
			"group": "Simple Services",
			"checker_type": "checkers.testchecker.TestCheckerNotAvailable"
		}
        '''
        res = create_service('fake1', json.loads(cfg))
        self.assertEqual('fake1', res['service_name'])
        self.assertEqual('NoneType', type(res['checker_type_class']).__name__)
        self.assertEqual(None, res['checker'])
        
        # missing required args
        cfg = '''
        {	
			"group": "Simple Services",
			"checker_type": "checkers.testchecker.TestChecker",
			"checker_args": {
				"return_value_wrong": "4711"
			}
		}
        '''
        res = create_service('fake1', json.loads(cfg))
        self.assertEqual('fake1', res['service_name'])
        # due to wrong arguments
        self.assertEqual(None, res['checker'])
        
    def test_create_service_info_simple(self):
        cfg = '''
        {	
			"group": "Simple Services",
			"checker_type": "checkers.testchecker.TestChecker",
			"checker_args": {
				"return_value": true
			},
            "info_type": "info.testinfo.TestInfo",
			"info_args": {
				"result": "4711"
			}
		}
        '''
        res = create_service('fake', json.loads(cfg))
        self.assertEqual('fake', res['service_name'])
        
        self.assertEqual('info.testinfo.TestInfo', res['info_type'])
        
        # defines a type
        self.assertEqual('type', type(res['info_type_class']).__name__)
        self.assertEqual('TestInfo', type(res['info']).__name__)
        
    def test_create_service_info_error(self):
        # unknown type
        cfg = '''
        {	
			"group": "Simple Services",
			"checker_type": "checkers.testchecker.TestChecker",
			"checker_args": {
				"return_value": true
			},
            "info_type": "info.testinfo.TestInfoNotAvailable"
		}
        '''
        res = create_service('fake', json.loads(cfg))
        self.assertEqual('NoneType', type(res['info_type_class']).__name__)
        self.assertEqual(None, res['info'])
        
        # wrong arguments
        cfg = '''
        {	
			"group": "Simple Services",
			"checker_type": "checkers.testchecker.TestChecker",
			"checker_args": {
				"return_value": true
			},
            "info_type": "info.testinfo.TestInfo",
            "info_args": {
				"command": "echo"
			}
		}
        '''
        res = create_service('fake', json.loads(cfg))
        self.assertEqual(None, res['info'])
        
        