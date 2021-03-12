import unittest
from unittest.mock import patch

from logs_parser import LogsParser
from logs_analyzer import LogsAnalyzer


class TestLogsParser(unittest.TestCase):
    """Тестирование класса LogsParser."""
    def setUp(self):
        self.logs_parser = LogsParser()

    def test_mock_patch(self):
        """Тест работы функции 'patch' (для ознакомления)."""
        with patch('logs_parser.LogsParser.get_data_from_logs_server') as mock_get:
            mock_get.return_value.status_code = 200
            response = self.logs_parser.get_data_from_logs_server()
            self.assertEqual(response.status_code, 200)


class TestLogsAnalyzer(unittest.TestCase):
    """Тестирование класса LogsAnalyzer."""
    test_cases = {
        'wrong_date': ['00000000', None],
        'correct_date': ['20210312', None]
    }

    def setUp(self):
        self.logs_analyzer = LogsAnalyzer()

    def test_user_input_right_len(self):
        """Тест функции валидации даты на группе сабтестов с корректной длиной даты."""
        for name, (input_date, answer) in self.test_cases.items():
            with self.subTest(name=name):
                self.assertEqual(self.logs_analyzer._date_validation(input_date), answer)

    def test_user_input_wrong_len(self):
        """Тест функции валидации даты на дате с некорректной длиной."""
        with self.assertRaises(ValueError):
            self.logs_analyzer._date_validation('1234')

    def test_error_in_log(self):
        """Тест функции поиска ошибок в логе на тест-кейсе с ошибкой."""
        test_data = {'error': 'created_day: does not match format 20200105 (year - 2021, month - 01, day — 05)'}
        self.assertEqual(self.logs_analyzer._errors_in_log(test_data), True)

    def test_without_error_in_log(self):
        """Тест функции поиска ошибок в логе на тест-кейсе без ошибки."""
        test_data = {'error': '', 'logs': 'not empty'}
        self.assertEqual(self.logs_analyzer._errors_in_log(test_data), False)

    def test_sort_logs(self):
        """Тест функции сортировки лога с использованием 'mock patch'."""
        logs_parser = LogsParser()

        with patch('logs_parser.LogsParser.get_data_from_logs_server') as mock_get:
            mock_get.return_value = {
                'logs': [
                    {'created_at': '2021-01-23T17:12:03', 'name': 'Jorah'},
                    {'created_at': '2021-01-23T17:12:01', 'name': 'Jaime'},
                    {'created_at': '2021-01-23T17:12:02', 'name': 'Drogo'},
                ]
            }

            fake_response = logs_parser.get_data_from_logs_server()
            self.logs_analyzer._sort_logs(fake_response)

            expected_response = {
                'logs': [
                    {'created_at': '2021-01-23T17:12:01', 'name': 'Jaime'},
                    {'created_at': '2021-01-23T17:12:02', 'name': 'Drogo'},
                    {'created_at': '2021-01-23T17:12:03', 'name': 'Jorah'},
                ]
            }

            self.assertEqual(expected_response, fake_response)


if __name__ == '__main__':
    unittest.main()
