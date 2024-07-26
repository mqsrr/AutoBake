import threading
import time

import schedule

from backend.Models.Order import Order
from backend.Models.OrderState import OrderState
from backend.Models.Pizza import Pizza
from backend.Services.Oven import Oven


def execute_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


class OvenService:
    def __init__(self, ovens: [Oven]):
        self.ovens = ovens
        self.pizza_queue = []
        self.order_queue = []

        schedule.every().second.do(self.try_cook_pizza)
        schedule.every().second.do(self.check_order_state)

        self.thread = threading.Thread(target=execute_scheduler)
        self.thread.start()

    def add_pizza_into_queue(self, pizza: Pizza) -> None:
        self.pizza_queue.append(pizza)

    def add_order_into_queue(self, order: Order) -> None:
        order_pizzas = []
        for pizza in order.pizzas:
            for i in range(pizza.quantity):
                pizza_to_add = Pizza(order.id, pizza.title, 1)

                order_pizzas.append(pizza_to_add)
                self.pizza_queue.append(pizza_to_add)

        order.order_state = OrderState.PENDING
        order.pizzas = order_pizzas
        self.order_queue.append(order)

    def check_order_state(self):
        if len(self.order_queue) == 0:
            return

        cooked_pizzas = []
        for order in self.order_queue:
            for pizza in order.pizzas:
                if pizza.cooking_time <= 1:
                    cooked_pizzas.append(pizza)

                elif pizza.cooking_time <= 9 and order.order_state != OrderState.PROCESSING:
                    order.order_state = OrderState.PROCESSING

            if cooked_pizzas == order.pizzas:
                order.order_state = OrderState.DONE
                time.sleep(2)
                self.order_queue.remove(order)

    def try_cook_pizza(self) -> None:
        if len(self.pizza_queue) == 0:
            return

        for oven in self.ovens:
            if len(oven.pizzas_to_cook) != 5:
                oven.insert_pizza(self.pizza_queue.pop(0))

            if len(self.pizza_queue) == 0:
                return

    def __del__(self) -> None:
        self.thread.join()
        for oven in self.ovens:
            del oven
