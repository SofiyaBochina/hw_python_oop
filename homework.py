from __future__ import annotations

import datetime as dt
from typing import List, Dict, Optional, Union


FORMAT: str = '%d.%m.%Y'
CURRENCIES: (Dict[str,
             Dict[str, Union[float, str]]]) = {'usd': {'value': 60,
                                                       'name': 'USD'},
                                               'eur': {'value': 70,
                                                       'name': 'Euro'},
                                               'rub': {'value': 1,
                                                       'name': 'руб'}}
CASH_BALANCE: str = 'На сегодня осталось {balance:.2f} {currency_name}'
DUTY_BALANCE: str = ('Денег нет, держись: '
                     'твой долг - {balance:.2f} {currency_name}')


class Record:
    """Класс записей."""

    def __init__(self, amount: int = 0, comment: str = "Неизвестно",
                 date: Optional[str] = None) -> None:
        """Конструктор класса Record, создаёт свойства для объекта
        и придаёт нужной формат дате записи,
        при необходимости записывая туда текущую дату.
        """
        self.amount = amount
        self.comment = comment
        if date is not None:
            record_date: dt.datetime = dt.datetime.strptime(date, FORMAT)
            self.date = record_date.date()
        else:
            self.date = dt.date.today()


class Calculator:
    """Родительский класс калькуляторов."""

    def __init__(self, limit: float = 0) -> None:
        """Конструктор класса, создаёт свойство лимита для объекта
        и пустой список записей.
        """

        self.limit = limit
        self.records: List[Record] = []

    def add_record(self, record: Record) -> None:
        """Метод, добавляющий новый объект
        класса Record в список records.
        """

        self.records.append(record)

    def get_today_stats(self) -> int:
        """Метод, возвращающий количество
        потребленных калорий/денег за сегодня.
        """

        today_stats: int = sum(record.amount for record in self.records
                               if record.date == dt.date.today())
        return today_stats

    def get_week_stats(self) -> int:
        """Метод, возвращающий количество
        потребленных калорий/денег за последние 7 дней.
        """

        week_stats: int = sum(record.amount for record in self.records
                              if (record.date > dt.date.today()
                                  - dt.timedelta(days=7)
                                  and record.date <= dt.date.today()))
        return week_stats

    def get_amount_remained(self):
        """Метод, возвращающий количество
        оставшихся калорий или денег.
        """

        amount_remained: Union[int, float] = (self.limit
                                              - self.get_today_stats())
        return amount_remained


class CaloriesCalculator(Calculator):
    """Класс-потомок класса Calculator,
    отвечающий за калькуляторы калорий.
    """

    def get_calories_remained(self) -> str:
        """Метод, возвращающий сообщение о текущем состоянии
        "баланса" калорий на сегодня.
        """

        if self.limit > self.get_today_stats():
            calories_remained: str = ('Сегодня можно съесть что-нибудь ещё, '
                                      'но с общей калорийностью не более '
                                      f'{self.get_amount_remained()} кКал')
            return calories_remained
        return 'Хватит есть!'


class CashCalculator(Calculator):
    """Класс-потомок класса Calculator,
    отвечающий за калькуляторы денег. В теле содержатся
    константы курсов валют.
    """

    USD_RATE: Union[float, int] = 60.0
    EURO_RATE: Union[float, int] = 70.0

    def get_today_cash_remained(self, currency: str) -> str:
        """Метод, возвращающий сообщение о текущем состоянии
        баланса денег в требуемой валюте на сегодня.
        """

        cash_remained: str

        for item, info in CURRENCIES.items():
            if item == currency:
                balance: Union[int, float] = (self.get_amount_remained()
                                              / info['value'])
                name: str = info['name']

        if self.limit == self.get_today_stats():
            return 'Денег нет, держись'
        elif self.limit > self.get_today_stats():
            cash_remained = CASH_BALANCE.format(balance=balance,
                                                currency_name=name)
            return cash_remained
        cash_remained = DUTY_BALANCE.format(balance=-balance,
                                            currency_name=name)
        return cash_remained


cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))

print(cash_calculator.get_today_cash_remained('eur'))
