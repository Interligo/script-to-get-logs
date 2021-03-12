import os

import requests
from requests.exceptions import InvalidURL
from requests.exceptions import MissingSchema

from logger_settings import logger


class LogsParser:
    """
==============================================================
Класс предназначен для получения данных со стороннего ресурса.
==============================================================
    """

    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/88.0.4324.190 Safari/537.36'
        }
        self.logs_url = 'http://www.dsdev.tech/logs/'

    def get_data_from_logs_server(self, date_to_search: str) -> dict:
        """Функция делает запрос к стороннему ресурсу и получает с него логи за конкретный день."""
        try:
            response = self.session.get(os.path.join(self.logs_url + date_to_search), headers=self.headers)
            if response.status_code == 200:
                log_data = response.json()
                logger.debug(f'Запрошены логи за дату: {date_to_search}.')
                logger.debug(f'Получен ответ: {log_data}.')
                return log_data
            else:
                logger.critical(f'{self.logs_url} не отвечает.')
                raise SystemExit(f'{self.logs_url} не отвечает.')
        except (InvalidURL, MissingSchema):
            logger.critical(f'Не удалось подключиться к {self.logs_url}.')
            raise SystemExit(f'Не удалось подключиться к {self.logs_url}.')
