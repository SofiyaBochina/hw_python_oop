from __future__ import annotations

import datetime as dt
from typing import List, Dict, Tuple, Optional, Union


FORMAT: str = '%d.%m.%Y'
CURRENCIES: (Dict[str,
             Tuple[Union[float, str]]]) = {'usd': (60, 'USD'),
                                           'eur': (70, 'Euro'),
                                           'rub': (1, 'руб')}
CAL_BALANCE: str = ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    '{balance} кКал')
CASH_BALANCE: str = 'На сегодня осталось {balance:.2f} {currency_name}'
DUTY_BALANCE: str = ('Денег нет, держись: '
                     'твой долг - {balance:.2f} {currency_name}')
STOP_EAT: str = 'Хватит есть!'
STOP_SPEND: str = 'Денег нет, держись'


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

    def get_amount_remained(self) -> Union[int, float]:
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
            balance = self.get_amount_remained()
            calories_remained: str = CAL_BALANCE.format(balance=balance)
            return calories_remained
        return STOP_EAT


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
                                              / info[0])
                name: str = info[1]

        if self.limit == self.get_today_stats():
            return STOP_SPEND
        elif self.limit > self.get_today_stats():
            cash_remained = CASH_BALANCE.format(balance=balance,
                                                currency_name=name)
            return cash_remained
        cash_remained = DUTY_BALANCE.format(balance=-balance,
                                            currency_name=name)
        return cash_remained
