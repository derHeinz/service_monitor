import unittest
import json

from service_creator import create_service, create_services

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

    def test_create_services_simple(self):
        cfg = '''
        {
            "services": {
                "test-true": {
                    "group": "Simple Services",
                    "checker_type": "checkers.testchecker.TestChecker",
                    "checker_args": {
                        "return_value": true
                    }
                },
                "test-false": {
                    "group": "Simple Services",
                    "checker_type": "checkers.testchecker.TestChecker",
                    "checker_args": {
                        "return_value": false
                    }
                }
            }
		}
        '''
        res = create_services(json.loads(cfg))
        self.assertEqual(2, len(res))
        self.assertEqual("test-true", res[0]['service_name'])
        self.assertEqual("Simple Services", res[0]['service_group'])
        self.assertEqual("test-false", res[1]['service_name'])
        self.assertEqual("Simple Services", res[1]['service_group'])


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

    def test_service_enablement(self):
        cfg_with_placeholder = '''
        {{	
			"group": "Simple Services",
            "enabled": {},
			"checker_type": "checkers.testchecker.TestChecker",
			"checker_args": {{
				"return_value": true
			}}
		}}
        '''
        
        # some false values
        res = create_service('fake', json.loads(cfg_with_placeholder.format("\"false\"")))
        self.assertEqual(False, res['enabled'])
        
        res = create_service('fake', json.loads(cfg_with_placeholder.format("\"False\"")))
        self.assertEqual(False, res['enabled'])
    
        res = create_service('fake', json.loads(cfg_with_placeholder.format("false")))
        self.assertEqual(False, res['enabled'])

        # some true values
        res = create_service('fake', json.loads(cfg_with_placeholder.format("\"true\"")))
        self.assertEqual(True, res['enabled'])
        
        res = create_service('fake', json.loads(cfg_with_placeholder.format("\"True\"")))
        self.assertEqual(True, res['enabled'])
        
        res = create_service('fake', json.loads(cfg_with_placeholder.format("true")))
        self.assertEqual(True, res['enabled'])
        
        res = create_service('fake', json.loads(cfg_with_placeholder.format("\"engage\"")))
        self.assertEqual(True, res['enabled'])
        

    def test_enabled_if_not_mentioned(self):
        # true even if enabled is not mentioned.
        cfg_enabled_not_mentioned = '''
        {	
			"group": "Simple Services",
			"checker_type": "checkers.testchecker.TestChecker",
			"checker_args": {
				"return_value": true
			}
		}
        '''
        res = create_service('fake', json.loads(cfg_enabled_not_mentioned))
        self.assertEqual(True, res['enabled'])

    def test_query_info(self):
        cfg_with_placeholder = '''
        {{	
			"group": "Simple Services",
            "query_info_even_if_offline": {},
			"checker_type": "checkers.testchecker.TestChecker",
			"checker_args": {{
				"return_value": true
			}}
		}}
        '''
        
        # some true values
        res = create_service('fake', json.loads(cfg_with_placeholder.format("true")))
        self.assertEqual(True, res['query_info_even_if_offline'])
        
        res = create_service('fake', json.loads(cfg_with_placeholder.format("\"true\"")))
        self.assertEqual(True, res['query_info_even_if_offline'])
        
        res = create_service('fake', json.loads(cfg_with_placeholder.format("\"True\"")))
        self.assertEqual(True, res['query_info_even_if_offline'])
        
        # some false values
        res = create_service('fake', json.loads(cfg_with_placeholder.format("false")))
        self.assertEqual(False, res['query_info_even_if_offline'])
        
        res = create_service('fake', json.loads(cfg_with_placeholder.format("\"false\"")))
        self.assertEqual(False, res['query_info_even_if_offline'])
        
        res = create_service('fake', json.loads(cfg_with_placeholder.format("\"False\"")))
        self.assertEqual(False, res['query_info_even_if_offline'])

    def test_query_info_if_not_mentioned(self):
        cfg = '''
        {	
			"group": "Simple Services",
			"checker_type": "checkers.testchecker.TestChecker",
			"checker_args": {
				"return_value": true
			}
		}
        '''
        res = create_service('fake', json.loads(cfg))
        self.assertEqual(False, res['query_info_even_if_offline'])
