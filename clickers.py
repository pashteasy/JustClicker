import random
import time

import pyautogui as auto
import pynput.keyboard as pk
import pynput.mouse as pm


class Clicker:
    def __init__(self):
        self.coordinates = []
        self.is_clicking = False
        self.random_delay = False

    def reset_coordinates(self):
        self.coordinates.clear()

    def toggle_clicking(self):
        self.is_clicking = not self.is_clicking


class PyAutoGuiClicker(Clicker):
    def __init__(self, btn_to_press):
        super().__init__()
        self.btn_to_press = btn_to_press

    def click(self, click_delay):
        for coord in self.coordinates:
            if not self.is_clicking:
                return
            auto.moveTo(coord[0], coord[1])
            auto.click(button=self.btn_to_press)
            delay = click_delay + random.uniform(0, click_delay) if self.random_delay else click_delay
            time.sleep(delay)

    def add_current_position(self):
        x, y = auto.position()
        self.coordinates.append((x, y))
        return x, y


class KeyboardClicker(Clicker):
    def __init__(self, key_to_press: pk.Key | str):
        super().__init__()
        self.keyboard = pk.Controller()
        self.key_to_press = key_to_press

    def click(self, click_delay):
        if not self.is_clicking:
            return
        self.keyboard.press(self.key_to_press)
        time.sleep(0.1)
        self.keyboard.release(self.key_to_press)
        delay = click_delay + random.uniform(0, click_delay) if self.random_delay else click_delay
        time.sleep(delay)

    def add_current_position(self):
        x, y = 0, 0
        self.coordinates.append((x, y))
        return x, y


class PynputClicker(Clicker):
    def __init__(self, btn_to_press):
        super().__init__()
        self.mouse = pm.Controller()
        self.btn_to_press = btn_to_press

    def click(self, click_delay):
        for coord in self.coordinates:
            if not self.is_clicking:
                return
            self.mouse.position = (coord[0], coord[1])
            self.mouse.press(button=self.btn_to_press)
            time.sleep(0.1)
            self.mouse.release(button=self.btn_to_press)
            delay = click_delay + random.uniform(0, click_delay) if self.random_delay else click_delay
            time.sleep(delay)

    def add_current_position(self):
        x, y = self.mouse.position
        self.coordinates.append((x, y))
        return x, y