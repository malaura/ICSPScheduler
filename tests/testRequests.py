from code import Requests
import unittest


class TestRequests(unittest.TestCase):

    def test_request_get_name(self):
        request = Requests.Request('test', '11/25/2017', '00:00', '02:00', '00:00', '00:00')
        get_name = request.get_name()
        self.assertEqual(get_name, 'test')

    def test_request_get_date(self):
        request = Requests.Request('test', '11/25/2017', '00:00', '02:00', '00:00', '00:00')
        get_date = request.get_date()
        self.assertEqual(get_date, '11/25/2017')

    def test_request_get_start_time(self):
        request = Requests.Request('test', '11/25/2017', '00:00', '02:00', '00:00', '00:00')
        get_start_time = request.get_start_time()
        self.assertEqual(get_start_time, '00:00')

    def test_request_get_end_time(self):
        request = Requests.Request('test', '11/25/2017', '00:00', '02:00', '00:00', '00:00')
        get_end_time = request.get_end_time()
        self.assertEqual(get_end_time, '02:00')

    def test_request_get_buffer_start(self):
        request = Requests.Request('test', '11/25/2017', '00:00', '02:00', '00:00', '00:00')
        get_buffer_start = request.get_buffer_start()
        self.assertEqual(get_buffer_start, '00:00')

    def test_request_get_buffer_end(self):
        request = Requests.Request('test', '11/25/2017', '00:00', '02:00', '00:00', '00:00')
        get_buffer_end = request.get_buffer_end()
        self.assertEqual(get_buffer_end, '00:00')

    def test_request_get_actual_start_time(self):
        request = Requests.Request('test', '11/25/2017', '00:00', '02:00', '00:00', '00:00')
        get_actual_start_time = request.get_actual_start_time()
        self.assertEqual(get_actual_start_time, 0.0)

    def test_request_get_actual_end_time(self):
        request = Requests.Request('test', '11/25/2017', '00:00', '02:00', '00:00', '00:00')
        get_actual_end_time = request.get_actual_end_time()
        self.assertEqual(get_actual_end_time, 2.0)

    def test_request_get_dictionary(self):
        requests = Requests()
        self.assertEqual(len(requests.get_dictionary()), 0)

