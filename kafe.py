"""Моделирование работы сети кафе с несколькими столиками и потоком посетителей, прибывающих для заказа пищи и уходящих после завершения приема.

Есть сеть кафе с несколькими столиками. Посетители приходят, заказывают еду, занимают столик,
 употребляют еду и уходят. Если столик свободен, новый посетитель принимается к обслуживанию,
иначе он становится в очередь на ожидание.

Создайте 3 класса:
Table - класс для столов, который будет содержать следующие атрибуты: number(int) - номер стола,
 is_busy(bool) - занят стол или нет.

Cafe - класс для симуляции процессов в кафе. Должен содержать следующие атрибуты и методы:
Атрибуты queue - очередь посетителей (создаётся внутри init), tables список столов (поступает из вне).
Метод customer_arrival(self) - моделирует приход посетителя(каждую секунду).
Метод serve_customer(self, customer) - моделирует обслуживание посетителя. Проверяет наличие
свободных столов, в случае наличия стола - начинает обслуживание посетителя (запуск потока),
в противном случае - посетитель поступает в очередь. Время обслуживания 5 секунд.
Customer - класс (поток) посетителя. Запускается, если есть свободные столы.

Так же должны выводиться текстовые сообщения соответствующие событиям:
Посетитель номер <номер посетителя> прибыл.
Посетитель номер <номер посетителя> сел за стол <номер стола>. (начало обслуживания)
Посетитель номер <номер посетителя> покушал и ушёл. (конец обслуживания)
Посетитель номер <номер посетителя> ожидает свободный стол. (помещение в очередь)"""

import threading
from threading import Thread
import time
import queue


class Table:
    # Класс Table содержит атрибуты number (номер стола) и is_busy (занят стол или нет).
    def __init__(self, number=int, is_busy=bool):

        self.number = number
        self.is_busy = is_busy
        super().__init__()


    def run(self):
        if self.is_busy == True:
            print(f"Свободен  {self.number} столик.")
        else:
            print(f"Занят  {self.number} столик.")


class Cafe:
    #   Класс Cafe- класс для симуляции процессов в кафе/содержит атрибуты:
    def __init__(self, tables):
        self.q = queue.Queue(maxsize=3)
        self.tables = tables
        super().__init__()


    def customer_arrival(self):
        """моделирует приход посетителя(каждую секунду)"""
        self.customer = 0
        while self.customer < 20: # Цикл продолжается, пока количество посетителей не достигнет 20 (ограничение на количество посетителей).
            self.customer += 1
            print(f"Посетитель {self.customer} прибыл.")
            self.serv_customer(self.customer)
            time.sleep(1) # Программа ждет 1 секунду перед обработкой следующего посетителя.


    def serv_customer(self, customer):
        """моделирует обслуживание посетителя.
        Проверяет наличие свободных столов, в случае наличия стола -
         начинает обслуживание посетителя (запуск потока),
         в противном случае - посетитель поступает в очередь. Время обслуживания 3 секундs."""

        self.q.put(customer)
        for i in range(len(tables)):
            g_tables = tables[i].is_busy
            if g_tables == True:
                while not self.q.empty():
                    Customer(i + 1, self.q.get()).start()


class Customer(Thread):
    """Запускается, если есть свободные столы."""
    def __init__(self, table, customer):
        super().__init__()
        self.customer = customer
        self.table = table

    def run(self):

        print(f"Посетитель номер {self.customer} сел за стол {self.table}.")
        tables[self.table - 1].is_busy = False
        if tables[self.table - 1].is_busy == False:
            print(f"Столик {self.table} занят")
        time.sleep(3)
        print(f"Посетитель номер {self.customer} покушал и ушёл.")
        tables[self.table - 1].is_busy = True


# Создаем столики в кафе

table1 = Table(1, is_busy=True)
table2 = Table(2, is_busy=True)
table3 = Table(3, is_busy=True)
tables = [table1, table2, table3]
# Инициализируем кафе
cafe = Cafe(tables)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

# Ожидаем завершения работы прибытия посетителей
customer_arrival_thread.join()