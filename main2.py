import time
import keyboard as key
import random
import threading
from pynput.mouse import Button, Controller
from tkinter import Tk, Label, Entry, Checkbutton, BooleanVar, Button as TkButton, messagebox

window = Tk()
window.title("JustClicker")
window.geometry('320x140')

lb_click_delay = Label(window, text='Click interval (ms):', font=("Arial", 12))
lb_hotkey = Label(window, text='Hot key start/pause:', font=("Arial", 12))
lb_space = Label(window, text='Space', font=("Arial", 12))
lb_save = Label(window, text='Save coordinates:', font=("Arial", 12))
lb_alt = Label(window, text='Tab', font=("Arial", 12))

lb_click_delay.grid(column=0, row=0)
lb_hotkey.grid(column=0, row=1)
lb_space.grid(column=1, row=1)
lb_save.grid(column=0, row=3)
lb_alt.grid(column=1, row=3)

txt = Entry(window, width=7)
txt.grid(column=1, row=0)
txt.insert(0, '1000')  # Устанавливаем значение по умолчанию

random_delay = Checkbutton(window, text='Random delay')
random_delay.grid(column=2, row=0)

coordinates = []

status_label = Label(window, text='', font=("Arial", 12), fg='green')
status_label.grid(column=0, row=6, columnspan=3)

mouse = Controller()


def click(t):
    for coord in coordinates:
        if not isClicking:
            return
        mouse.position = (coord[0], coord[1])
        mouse.click(Button.left, 2)
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
                click(t)
            except ValueError:
                messagebox.showerror('Error', 'Enter a valid Float value')
        time.sleep(0.01)


def save_coordinates():
    x, y = mouse.position
    coordinates.append((x, y))
    status_label.config(text=f'Coordinates saved: ({x}, {y})')


def start_click_thread():
    thread = threading.Thread(target=main)
    thread.daemon = True
    thread.start()


btn_reset = TkButton(window, text='Reset Coordinates', command=lambda: coordinates.clear(), font=("Arial", 12))
btn_reset.grid(column=0, row=5)

btn_toggle_clicker = TkButton(window, text='Start', command=set_clicker, font=("Arial", 12))
btn_toggle_clicker.grid(column=2, row=5)

txt.focus()
isClicking = False
random_delay.var = BooleanVar()
random_delay.config(variable=random_delay.var)

key.add_hotkey('space', set_clicker)
key.add_hotkey('tab', save_coordinates)

start_click_thread()  # Запуск основного потока сразу при старте программы

window.mainloop()