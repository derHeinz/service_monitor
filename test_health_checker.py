import unittest

from health_checker import check_health, SERVICE_INFO_NOT_CONFIGURED, SERVICE_STATE_DEFAULT, SERVICE_INFO_ERROR_PREFIX, SERVICE_INFO_DEACTIVATED, SERVICE_INFO_STATE_DISABLED


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


class Testhealth_checker(unittest.TestCase):
    '''
    Tests
    # check health online(True), offline(False) and error
    # check info
    # query_info_even_if_offline, not present and set to true
    '''
    def assertFirstTwoEqualLastNotNoneAndSizeIs3(self, result, state, info):
        self.assertEqual(3, len(result))
        self.assertEqual(state, result[0])
        self.assertEqual(info, result[1])
        self.assertIsNotNone(result[2])

    def test_checker(self):

        cfg = {'service_name': 'test', 'enabled': True, 'checker_type': 'Test', 'checker': TrueChecker(), 'service_config': None}
        self.assertFirstTwoEqualLastNotNoneAndSizeIs3(check_health(cfg), True, SERVICE_INFO_NOT_CONFIGURED)

        cfg = {'service_name': 'test', 'enabled': True, 'checker_type': 'Test', 'checker': FalseChecker(), 'service_config': None}
        self.assertFirstTwoEqualLastNotNoneAndSizeIs3(check_health(cfg), False, SERVICE_INFO_NOT_CONFIGURED)

        # check when checker throws exception
        cfg = {'service_name': 'test', 'enabled': True, 'checker_type': 'Test', 'checker': ExceptionChecker(), 'service_config': None}
        self.assertFirstTwoEqualLastNotNoneAndSizeIs3(check_health(cfg), SERVICE_STATE_DEFAULT, SERVICE_INFO_NOT_CONFIGURED)

    def test_info_checker(self):

        cfg = {'service_name': 'test', 'enabled': True, 'checker_type': 'Test', 'checker': TrueChecker(),
               'info_type': 'Test', 'info':  SimpleInfo(), 'service_config': None}
        self.assertFirstTwoEqualLastNotNoneAndSizeIs3(check_health(cfg), True, "Test")

        # check with info throws exception
        cfg = {'service_name': 'test', 'enabled': True, 'checker_type': 'Test', 'checker': TrueChecker(),
               'info_type': 'Test', 'info':  ExceptionInfo(), 'service_config': None}
        res = check_health(cfg)
        self.assertTrue(res[0])
        self.assertTrue(res[1].startswith(SERVICE_INFO_ERROR_PREFIX))

    def test_info_checker_query_info_even_if_offline(self):

        # don't check when result is False
        cfg = {'service_name': 'test', 'enabled': True, 'checker_type': 'Test', 'checker': FalseChecker(),
               'info_type': 'Test', 'info':  SimpleInfo(), 'query_info_even_if_offline': False}
        self.assertFirstTwoEqualLastNotNoneAndSizeIs3(check_health(cfg), False, SERVICE_INFO_DEACTIVATED)

        # do check when extra flag is True
        cfg = {'service_name': 'test', 'enabled': True, 'checker_type': 'Test', 'checker': FalseChecker(),
               'info_type': 'Test', 'info':  SimpleInfo(), 'query_info_even_if_offline': True}
        self.assertFirstTwoEqualLastNotNoneAndSizeIs3(check_health(cfg), False, "Test")

    def test_disabled(self):

        cfg = {'service_name': 'test', 'enabled': False, 'checker_type': 'Test', 'checker': TrueChecker(),
               'info_type': 'Test', 'info':  SimpleInfo(), 'query_info_even_if_offline': False}

        self.assertFirstTwoEqualLastNotNoneAndSizeIs3(check_health(cfg), None, SERVICE_INFO_STATE_DISABLED)
