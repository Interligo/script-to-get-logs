from datetime import datetime

from logs_parser import LogsParser
from db_management import DataBaseManager
from logger_settings import logger


class LogsAnalyzer:
    """
============================================================
Класс предназначен для анализа данных со стороннего ресурса.
============================================================
    """

    def __init__(self):
        self.logs_parser = LogsParser()
        self.logs_date = None
        self.db = None

    def _date_validation(self, input_date: str) -> None:
        """Функция проверяет дату на корректный формат и поднимает исключение, если дата некорректна."""
        # Можно воспользоваться возможностями 'datetime.strptime', но, учитывая иные требования, решил велосипедить.
        if input_date.isdigit() and len(input_date) == 8:
            logger.debug('Введенная пользователем дата валидирована успешно.')
            self.logs_date = input_date
        else:
            logger.error(f'Пользователем введенна дата несоответствующего формата - {input_date}.')
            raise ValueError(f'Введенна дата несоответствующего формата - {input_date}.')

    def _array_partition(self, data: list, low: int, high: int) -> int:
        """Функция выбирает средний элемент в качестве опорного (сортирует слева направо по увеличению)."""
        middle = data[(low + high) // 2]
        i = low - 1
        j = high + 1

        while True:
            i += 1

            while data[i]['created_at'] < middle['created_at']:
                i += 1

            j -= 1
            while data[j]['created_at'] > middle['created_at']:
                j -= 1

            if i >= j:
                return j

            data[i], data[j] = data[j], data[i]

    def _sort_logs(self, raw_data: dict) -> dict:
        """Функция сортирует полученные логи по полю 'created_at'."""
        all_logs = raw_data['logs']

        def _quick_sort(array: list, low: int, high: int):
            """Вспомогательная рекурсивная функция для сортировки."""
            if low < high:
                middle_index = self._array_partition(array, low, high)
                _quick_sort(array, low, middle_index)
                _quick_sort(array, middle_index + 1, high)

        _quick_sort(all_logs, 0, len(all_logs) - 1)

        logger.info(f'Лог от {self.logs_date} отсортирован.')
        return all_logs

    def _errors_in_log(self, raw_data: dict) -> bool:
        """Функция проверяет лог на наличие ошибок."""
        if raw_data['error']:
            return True
        return False

    def make_analysis(self, input_date: str) -> str:
        """Функция-агрегатор объединяет в себе логику работы класса."""
        logger.info(f'Приступаю к анализу лога от {input_date}.')
        print(f'Приступаю к анализу лога от {input_date}.')

        self._date_validation(input_date)
        raw_data = self.logs_parser.get_data_from_logs_server(self.logs_date)

        if self._errors_in_log(raw_data):
            error_message = raw_data['error']
            logger.error(f'В логе обнаружена ошибка: {error_message}.')
            return f'Введенна дата несоответствующего формата - {self.logs_date}.'

        sorted_data = self._sort_logs(raw_data)

        if not self.db:
            self.db = DataBaseManager(self.logs_date)

        for row in sorted_data:
            creation_time = datetime.fromisoformat(row['created_at'])
            db_response = self.db.save_data_to_db(
                created_at=creation_time,
                first_name=row['first_name'],
                second_name=row['second_name'],
                message=row['message'],
                user_id=row['user_id']
            )
            logger.debug(db_response)

        logger.info(f'Разбор и сохранение лога от {self.logs_date} завершены успешно.')
        return f'Разбор и сохранение лога от {self.logs_date} завершены успешно.'

    def load_saved_logs(self, input_date: str):
        """Функция выгружает лог за конкретную дату из БД."""
        self._date_validation(input_date)
        if not self.db:
            self.db = DataBaseManager(self.logs_date)

        all_loaded_logs = self.db.get_all_data_from_db()
        return all_loaded_logs
