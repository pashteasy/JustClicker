import time
import keyboard as key
import random
import threading

from pynput.keyboard import Key, Controller as KeyboardController
from tkinter import Tk, Label, Entry, Checkbutton, BooleanVar, Button, messagebox

window = Tk()
window.title("JustClicker")
window.geometry('360x80')

lb_click_delay = Label(window, text='Click interval (ms):', font=("Arial Bold", 12))
lb_hotkey = Label(window, text='Hot key start/pause:', font=("Arial Bold", 12))
lb_space = Label(window, text='Space', font=("Arial Bold", 12))

lb_click_delay.grid(column=0, row=0)
lb_hotkey.grid(column=0, row=2)
lb_space.grid(column=1, row=2)


txt = Entry(window, width=7)
txt.grid(column=1, row=0)
txt.insert(0, '1000')  # Устанавливаем значение по умолчанию


random_delay = Checkbutton(window, text='Random delay')
random_delay.grid(column=2, row=0)


keyboard = KeyboardController()


def press(t):
    if not isClicking:
        return
    keyboard.press(Key.home)
    time.sleep(0.1)
    keyboard.release(Key.home)
    if random_delay.var.get():
        delay = t + random.uniform(0, t)
    else:
        delay = t
    time.sleep(delay)


def set_clicker():
    global isClicking
    isClicking = not isClicking
    update_button_text()


def update_button_text():
    if isClicking:
        btn_toggle_clicker.config(text='Pause')
    else:
        btn_toggle_clicker.config(text='Start')


def main():
    while True:
        if isClicking:
            try:
                t = float(txt.get()) / 1000  # Convert to seconds
                press(t)
            except ValueError:
                messagebox.showerror('Error', 'Enter a valid Float value')
        time.sleep(0.01)


def start_click_thread():
    thread = threading.Thread(target=main)
    thread.daemon = True
    thread.start()


btn_toggle_clicker = Button(window, text='Start', command=set_clicker, font=("Arial Bold", 12))
btn_toggle_clicker.grid(column=2, row=2)

isClicking = False
random_delay.var = BooleanVar()
random_delay.config(variable=random_delay.var)

key.add_hotkey('space', set_clicker)

start_click_thread()  # Запуск основного потока сразу при старте программы

window.mainloop()
