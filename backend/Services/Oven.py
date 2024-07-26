import csv
import os
import time
from datetime import datetime
from multiprocessing.pool import ThreadPool

import requests
from fhict_cb_01.custom_telemetrix import CustomTelemetrix
from flask import jsonify

from backend.Models.OvenState import OvenState
from backend.Models.Pizza import Pizza


def init_csv_file() -> None:
    with open('./order-history.csv', mode='w', newline='') as csv_file:
        fieldnames = ['board-id', 'pizza', 'created_at']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()


class Oven(object):
    LEDS = [4, 5, 6, 7]

    def __init__(self, board: CustomTelemetrix, id: int) -> None:
        self.id = id
        self.board = board
        self.thread_pool = ThreadPool(7)

        self.oven_state = OvenState.WAITING
        self.pizzas_to_cook = []
        self.cooking_queue = {}
        self.pizza_counter = 1

        self.setup_arduino_board()
        if os.path.exists('./order-history.csv'):
            init_csv_file()

        self.thread_pool.apply_async(func=self.start_listening)

    @property
    def oven_state(self) -> OvenState:
        return self._oven_state

    @oven_state.setter
    def oven_state(self, oven_state: OvenState) -> None:
        self._oven_state = oven_state
        self.enable_led(oven_state.value)

    def setup_arduino_board(self) -> None:
        self.setup_leds()
        self.board.displayOn()

        self.board.set_pin_mode_analog_output(3)
        self.board.set_pin_mode_digital_input_pullup(8)

    def setup_leds(self) -> None:
        for LED in self.LEDS:
            self.board.set_pin_mode_digital_output(LED)

    def enable_led(self, led_port: int) -> None:
        for LED in self.LEDS:
            self.board.digital_write(LED, 0)

        self.board.digital_write(led_port, 1)

    def display_oven_time(self, pizza: Pizza, seconds: int) -> None:
        current_time = seconds
        current_pizza_id = self.pizza_counter

        self.pizza_counter += 1
        self.cooking_queue[pizza] = current_pizza_id

        for i in range(seconds):
            current_pizza = min(self.cooking_queue.values())
            if current_pizza == current_pizza_id:
                self.board.displayShow(str(current_pizza_id) + '.' + str(current_time))

            pizza.cooking_time = current_time
            current_time -= 1

            time.sleep(1)

        self.cooking_queue.pop(pizza)
        self.pizzas_to_cook.remove(pizza)

        self.board.analog_write(3, 5)
        time.sleep(.2)
        self.board.analog_write(3, 0)

        if len(self.pizzas_to_cook) == 0:
            self.oven_state = OvenState.DONE
            self.board.displayShow('done')
            self.pizza_counter = 1
            time.sleep(.2)

        self.add_order_into_csv(pizza)
        self.send_pizza_response(pizza)

    def start_listening(self):
        while True:
            time.sleep(.3)
            button_data = self.board.digital_read(8)

            if button_data is None or button_data[0] == 1 or self.oven_state == OvenState.COOKING:
                continue

            if self.oven_state == OvenState.DONE:
                self.wait_for_pizza()
                continue

            elif self.oven_state == OvenState.READY_TO_START:
                self.start_cooking()
                continue

    def insert_pizza(self, pizza: Pizza) -> None:
        self.pizzas_to_cook.append(pizza)

        if self.oven_state == OvenState.COOKING:
            self.thread_pool.apply_async(func=self.display_oven_time, args=(pizza, 10))
            return
        elif self.oven_state == OvenState.DONE:
            self.oven_state = OvenState.COOKING
            time.sleep(.1)

            self.thread_pool.apply_async(func=self.display_oven_time, args=(pizza, 10))
            return

        self.oven_state = OvenState.READY_TO_START
        self.board.displayShow(len(self.pizzas_to_cook))

    def start_cooking(self) -> None:
        self.oven_state = OvenState.COOKING
        for pizza in self.pizzas_to_cook:
            self.thread_pool.apply_async(func=self.display_oven_time, args=(pizza, 10))

    def wait_for_pizza(self) -> None:
        self.oven_state = OvenState.WAITING
        self.board.displayClear()

    def add_order_into_csv(self, pizza: Pizza) -> None:
        with open('./order-history.csv', mode='a', newline='') as csv_file:
            fieldnames = ['board-id', 'pizza', 'created_at']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writerow({
                'board-id': self.id,
                'pizza': pizza.title,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

    @staticmethod
    def send_pizza_response(pizza: Pizza) -> None:
        requests.post('http://127.0.0.1:8080/pizza', data=jsonify(pizza.to_json()))

    def __del__(self):
        self.thread_pool.close()
        self.board.displayOff()
        self.board.shutdown()
