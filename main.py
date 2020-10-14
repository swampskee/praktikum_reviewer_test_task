import datetime as dt
import json  # Не должно оставаться неиспользуемых импортов

class Record:
    # Параметр "по-умолчанию" для даты не должен быть пустой строкой,
    # в этом случае хорошим решением было бы  использование:
    # def __init__(self, amount, comment, date=dt.datetime.now().date())
    # Это позволило бы упростить код ниже
    def __init__(self, amount, comment, date=dt.datetime.now().date()):
        self.amount=amount
        # C учетом доработок выше, строку можно было бы сократить до:
        # self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        #     if isinstance(date, str) else date
        self.date = dt.datetime.now().date() if not date else dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment=comment
class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records=[]
    def add_record(self, record):
        self.records.append(record)
    def get_today_stats(self):
        # Всё ниже можно заменить на генераторное выражение, что позволило бы
        # увеличить читаемость и увеличить производительность:
        # today_stats = sum(
        # record for record in self.records
        # if record.date == dt.datetime.now().date())
        today_stats=0
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats+Record.amount

        return today_stats
    def get_week_stats(self):
        week_stats=0
        today = dt.datetime.now().date()
        # По аналогии с get_today_stats() можно заменить всё на
        # генераторное выражение, при этом сократив два неравенства до одного
        # двойного:
        # 7 > (today - record.date).days >= 0
        for record in self.records:
            if (today -  record.date).days <7 and (today -  record.date).days >=0:
                week_stats +=record.amount
        return week_stats
class CaloriesCalculator(Calculator):
    def get_calories_remained(self): # Получает остаток калорий на сегодня
        x=self.limit-self.get_today_stats()
        # Else в таком варианте можно опустить, так как, в случае если x > 0,
        # уже есть return. Однобуквенные переменные уменьшают читаемость, лучше
        # давать названия в соответствии с логикой
        if x > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {x} кКал'
        else:
            return 'Хватит есть!'
class CashCalculator(Calculator):
    # Нет необходимости явного преобразования во float, Python сам преобразует
    # типы если это будет нужно
    USD_RATE=float(60) #Курс доллар США.
    EURO_RATE=float(70) #Курс Евро.
    # По заданию метод get_today_cash_remained должен принимать только один
    # аргумент currency, соответственно USD_RATE и EURO_RATE использовать через
    # self.USD_RATE и self.EURO_RATE соответственно
    def get_today_cash_remained(self, currency, USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type=currency
        cash_remained = self.limit - self.get_today_stats()
        if currency=='usd':
            cash_remained /= USD_RATE
            currency_type ='USD'
        elif currency_type=='eur':
            cash_remained /= EURO_RATE
            currency_type ='Euro'
        elif currency_type=='rub':
            # Это условие ничего не делает, возможно тут опечатка. Можно убрать
            # эту строку так как в случае с рублём мы не проводим конвертацию
            cash_remained == 1.00
            currency_type ='руб'
        if cash_remained > 0:
            return f'На сегодня осталось {round(cash_remained, 2)} {currency_type}'
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # Тут лучше использовать else вместо elif'a так как остальные варианты
        # мы обработали выше
        elif cash_remained < 0:
            # Код должен быть единообразным, если везде выше использовались
            # f-строки, то и тут надо бы переписать с .format'а
            return 'Денег нет, держись: твой долг - {0:.2f} {1}'.format(-cash_remained, currency_type)

    # Так как мы не расширяем метод никакой новой логикой, можно сразу
    # использовать родительский и не переопределять его здесь
    def get_week_stats(self):
        super().get_week_stats()

# По всему коду не соблюдается PEP8. Нет отступов между логическими частями и
# отдельными классами, присутствует превышение максимальной длины строки
# в 79 символов, не оформлены переносы строк. Для отслеживания таких проблем
# лучше всего сразу начать использовать линтеры(например pylint) и различные
# спеллчекеры
