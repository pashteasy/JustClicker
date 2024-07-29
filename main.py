import pyautogui as auto
import time
import keyboard as key
import random
from tkinter import *
from tkinter import messagebox
import threading
import json

window = Tk()
window.title("JustClicker")
window.geometry('360x180')

lb_click_delay = Label(window, text='Click interval (ms):', font=("Arial Bold", 12))
lb_cycle_delay = Label(window, text='Cycle delay (s):', font=("Arial Bold", 12))
lb_hotkey = Label(window, text='Hot key start/pause:', font=("Arial Bold", 12))
lb_space = Label(window, text='Space', font=("Arial Bold", 12))
lb_save = Label(window, text='Save coordinates:', font=("Arial Bold", 12))
lb_alt = Label(window, text='Tab', font=("Arial Bold", 12))

lb_click_delay.grid(column=0, row=0)
lb_cycle_delay.grid(column=0, row=1)
lb_hotkey.grid(column=0, row=2)
lb_space.grid(column=1, row=2)
lb_save.grid(column=0, row=4)
lb_alt.grid(column=1, row=4)

txt = Entry(window, width=7)
txt.grid(column=1, row=0)
txt.insert(0, '1000')  # Устанавливаем значение по умолчанию

txt_cycle_delay = Entry(window, width=7)
txt_cycle_delay.grid(column=1, row=1)
txt_cycle_delay.insert(0, '60')  # Устанавливаем значение по умолчанию

random_delay = Checkbutton(window, text='Random delay')
random_delay.grid(column=2, row=0)

coordinates = []

status_label = Label(window, text='', font=("Arial Bold", 12), fg='green')
status_label.grid(column=0, row=6, columnspan=3)

cycle_timer_label = Label(window, text='', font=("Arial Bold", 12), fg='red')
cycle_timer_label.grid(column=2, row=1, columnspan=3)


def click(click_delay, cycle_delay):
    for coord in coordinates:
        if not isClicking:
            return
        auto.moveTo(coord[0], coord[1])
        auto.click()
        if random_delay.var.get():
            click_delay += random.uniform(0, click_delay)
        time.sleep(click_delay)

    for remaining in range(int(cycle_delay), 0, -1):
        if not isClicking:
            cycle_timer_label.config(text="")
            return
        cycle_timer_label.config(text=remaining)
        time.sleep(1)
    cycle_timer_label.config(text='')


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
                click_delay = float(txt.get()) / 1000  # Convert to seconds
                cycle_delay = float(txt_cycle_delay.get())
                click(click_delay, cycle_delay)
            except ValueError:
                messagebox.showerror('Error', 'Enter a valid Float value')
        time.sleep(0.01)


def save_coordinates():
    x, y = auto.position()
    coordinates.append((x, y))
    status_label.config(text=f'Coordinates saved: ({x}, {y})')


def save_coordinates_to_file():
    with open('coordinates.txt', 'w') as file:
        json.dump(coordinates, file)
    status_label.config(text='Coordinates saved to file')


def load_coordinates_from_file():
    global coordinates
    try:
        with open('coordinates.txt', 'r') as file:
            coordinates = json.load(file)
        status_label.config(text='Coordinates loaded from file')
    except FileNotFoundError:
        messagebox.showerror('Error', 'No saved coordinates found')


def start_click_thread():
    thread = threading.Thread(target=main)
    thread.daemon = True
    thread.start()


btn_reset = Button(window, text='Reset crds', command=lambda: coordinates.clear(), font=("Arial Bold", 12))
btn_reset.grid(column=0, row=5)

btn_save_file = Button(window, text='Save crds', command=save_coordinates_to_file, font=("Arial Bold", 12))
btn_save_file.grid(column=1, row=5)

btn_load_file = Button(window, text='Load crds', command=load_coordinates_from_file, font=("Arial Bold", 12))
btn_load_file.grid(column=2, row=5)

btn_toggle_clicker = Button(window, text='Start', command=set_clicker, font=("Arial Bold", 12))
btn_toggle_clicker.grid(column=2, row=2)

isClicking = False
random_delay.var = BooleanVar()
random_delay.config(variable=random_delay.var)

key.add_hotkey('space', set_clicker)
key.add_hotkey('tab', save_coordinates)

start_click_thread()  # Запуск основного потока сразу при старте программы

window.mainloop()
