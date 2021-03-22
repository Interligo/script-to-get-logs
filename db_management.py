from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import TIMESTAMP
from sqlalchemy import TEXT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapper
from sqlalchemy.exc import OperationalError, InvalidRequestError

from db_models import LogsStorage


class DataBaseManager:
    """
=============================================================
Класс предназначен для взаимодействия с базой данных SQLite3.
=============================================================
    """

    def __init__(self, tablename: str):
        self.meta = MetaData()
        self.db_name = 'logs'
        self.table_name = tablename
        self.full_table_name = 'log_' + tablename
        self.meta.clear()
        self._clear_table_to_rewrite_log()
        self._create_table()

    def __str__(self):
        return f'База данных хранения логов.'

    def __repr__(self):
        return f'База данных хранения логов.'

    def _get_connection(self):
        """Функция возвращает подключение к SQLite3."""
        engine = create_engine(f'sqlite:///{self.db_name}.db', pool_pre_ping=True)
        return engine

    def _create_session(self):
        """Функция создает сессию для взаимодействия с базой данных."""
        engine = self._get_connection()
        db_session = sessionmaker(engine)
        session = db_session()
        return session

    def _create_table(self) -> None:
        """Функция создает таблицу из модели."""
        engine = self._get_connection()
        logs_table = Table(
            self.full_table_name,
            self.meta,
            Column('id', Integer, primary_key=True),
            Column('created_at', TIMESTAMP),
            Column('first_name', String),
            Column('second_name', String),
            Column('message', TEXT),
            Column('user_id', String),
            Column('errors', TEXT),
            extend_existing=True
        )
        self.meta.create_all(engine)
        mapper(LogsStorage, logs_table)

    def _clear_table_to_rewrite_log(self) -> None:
        """Удаляет таблицу с данными перед перезаписью лога за конкретную дату."""
        engine = self._get_connection()
        try:
            self.meta.reflect(bind=engine)
            table = self.meta.tables[self.full_table_name]
            if table is not None:
                self.meta.drop_all(engine, [table])
        except (OperationalError, KeyError):
            pass

    def save_data_to_db(self, created_at, first_name, second_name, message, user_id) -> str:
        """Сохраняет данные в БД."""
        session = self._create_session()

        new_data = LogsStorage(
            created_at=created_at,
            first_name=first_name,
            second_name=second_name,
            message=message,
            user_id=user_id
        )
        session.add(new_data)

        try:
            session.commit()
            return f'Данные от {created_at} успешно сохранены.'
        except OperationalError as error:
            return f'Возникла ошибка: {error}.'
        finally:
            session.close()

    def get_all_data_from_db(self):
        """Выгружает все данные из БД."""
        session = self._create_session()
        all_data = session.query(LogsStorage).all()
        session.close()
        return all_data
