class LogsStorage(object):
    """Модель БД для создания таблиц в базе данных."""
    __table_args__ = {'extend_existing': True}

    def __init__(self, created_at, first_name, second_name, message, user_id):
        self.created_at = created_at
        self.first_name = first_name
        self.second_name = second_name
        self.message = message
        self.user_id = user_id

    def __str__(self):
        return f'Лог от {self.created_at}'

    def __repr__(self):
        return f'\nЛог от {self.created_at}, {self.first_name}: {self.message}'

    def __getitem__(self, key):
        return getattr(self, key)
