from logs_analyzer import LogsAnalyzer


def main(input_date: str) -> str:
    """Функция дает доступ к публичному методу класса LogsAnalyzer и выводит результат."""
    logs = LogsAnalyzer()
    script_result = logs.make_analysis(input_date)
    return script_result


if __name__ == '__main__':
    input_date = input('Введите дату в формате "ггггммдд" для получения логов за этот день: ')
    print(main(input_date))
