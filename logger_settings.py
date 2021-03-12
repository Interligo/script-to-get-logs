import logging


def get_logger(name=__file__, file='script_logs.txt', encoding='utf-8'):
    """Функция для создания логгера, который записывает лог в файл."""
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')

    fh = logging.FileHandler(file, encoding=encoding)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    return log


logger = get_logger()
