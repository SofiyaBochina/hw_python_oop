from __future__ import annotations

import datetime as dt
from typing import List, Optional, Union


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
        if type(date) == str:
            record_date: dt.datetime = dt.datetime.strptime(date, '%d.%m.%Y')
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

        today_stats: int = 0
        for record in self.records:
            if record.date == dt.date.today():
                today_stats += record.amount
        return today_stats

    def get_week_stats(self) -> int:
        """Метод, возвращающий количество
        потребленных калорий/денег за последние 7 дней.
        """

        week_stats: int = 0
        for record in self.records:
            if (record.date > dt.date.today() - dt.timedelta(days=7)
                    and record.date <= dt.date.today()):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    """Класс-потомок класса Calculator,
    отвечающий за калькуляторы калорий.
    """

    def get_calories_remained(self) -> str:
        """Метод, возвращающий сообщение о текущем состоянии
        "баланса" калорий на сегодня.
        """

        if self.limit > self.get_today_stats():
            calories_remained: Union[int, float] = (self.limit
                                                    - self.get_today_stats())
            return('Сегодня можно съесть что-нибудь ещё, '
                   'но с общей калорийностью не более '
                   f'{calories_remained} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    """Класс-потомок класса Calculator,
    отвечающий за калькуляторы денег. В теле содержатся
    константы курсов валют.
    """

    USD_RATE: float = 72.74
    EURO_RATE: float = 84.32

    def get_today_cash_remained(self, currency: str) -> str:
        """Метод, возвращающий сообщение о текущем состоянии
        баланса денег в требуемой валюте на сегодня.
        """

        cash_remain: float
        cash_duty: float
        if self.limit == self.get_today_stats():
            return 'Денег нет, держись'
        elif self.limit > self.get_today_stats():
            if currency == 'usd':
                cash_remain = (self.limit
                               - self.get_today_stats()) / self.USD_RATE
                return f'На сегодня осталось {cash_remain:.2f} USD'
            elif currency == 'eur':
                cash_remain = ((self.limit - self.get_today_stats())
                               / self.EURO_RATE)
                return f'На сегодня осталось {cash_remain:.2f} Euro'
            cash_remain = self.limit - self.get_today_stats()
            return f'На сегодня осталось {cash_remain} руб'

        if currency == 'usd':
            cash_duty = (self.get_today_stats()
                         - self.limit) / self.USD_RATE
            return f'Денег нет, держись: твой долг - {cash_duty:.2f} USD'
        elif currency == 'eur':
            cash_duty = (self.get_today_stats()
                         - self.limit) / self.EURO_RATE
            return f'Денег нет, держись: твой долг - {cash_duty:.2f} Euro'
        cash_duty = self.get_today_stats() - self.limit
        return f'Денег нет, держись: твой долг - {cash_duty} руб'
