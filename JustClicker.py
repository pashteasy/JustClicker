import pyautogui as auto
import time
import keyboard as key
import random
from tkinter import *
from tkinter import messagebox

window = Tk()
window.title("JustClicker")
window.geometry('320x180')

lb_click_delay = Label(window, text='Click interval (ms):', font=("Arial Bold", 12))
lb_hotkey = Label(window, text='Hot key start/pause:', font=("Arial Bold", 12))
lb_exit = Label(window, text='Exit clicker mode:', font=("Arial Bold", 12))
lb_space = Label(window, text='Space', font=("Arial Bold", 12))
lb_esc = Label(window, text='Esc', font=("Arial Bold", 12))
lb_click_delay.grid(column=0, row=0)
lb_hotkey.grid(column=0, row=1)
lb_exit.grid(column=0, row=2)
lb_space.grid(column=1, row=1)
lb_esc.grid(column=1, row=2)
lb_save = Label(window, text='Save coordinates:', font=("Arial Bold", 12))
lb_save.grid(column=0, row=3)
lb_alt = Label(window, text='Alt', font=("Arial Bold", 12))
lb_alt.grid(column=1, row=3)

txt = Entry(window, width=7)
txt.grid(column=1, row=0)

random_delay = Checkbutton(window, text='Random delay')
random_delay.grid(column=1, row=4)

coordinates = []


def click(t):
    if random_delay.var.get():
        t = t + random.uniform(0, t)
    time.sleep(t)
    for coord in coordinates:
        auto.moveTo(coord[0], coord[1])
        auto.click()


def set_clicker():
    global isClicking
    isClicking = not isClicking


def main():
    try:
        t = float(txt.get())
        while True:
            if key.is_pressed('Esc'):
                break
            if isClicking:
                click(t / 1000)
    except ValueError:
        messagebox.showerror('Error', 'Enter a valid Float value')


def save_coordinates():
    x, y = auto.position()
    coordinates.append((x, y))
    messagebox.showinfo('Info', f'Coordinates saved: ({x}, {y})')


btn_start = Button(window, text='Start', command=main, font=("Arial Bold", 12))
btn_start.grid(column=0, row=4)

txt.focus()
isClicking = False
random_delay.var = BooleanVar()
random_delay.config(variable=random_delay.var)

key.add_hotkey('space', set_clicker)
key.add_hotkey('alt', save_coordinates)

window.mainloop()
