import tkinter as tk
from tkinter import ttk, messagebox
import keyboard as key
import json
import threading
import time
from pynput.keyboard import Key, Controller
from pynput.mouse import Button

import clickers

class KeyClickerGUI:
    def __init__(self, clicker):
        self.clicker = clicker
        self.window = tk.Tk()
        self.window.title("KeyClicker")
        self.window.geometry('320x80')

        self.lb_click_delay = tk.Label(self.window, text='Click interval (ms):', font=("Arial", 12))
        self.lb_hotkey = tk.Label(self.window, text='Hot key start/pause:', font=("Arial", 12))
        self.lb_space = tk.Label(self.window, text='Space', font=("Arial", 12))

        self.lb_click_delay.grid(column=0, row=0)
        self.lb_hotkey.grid(column=0, row=2)
        self.lb_space.grid(column=1, row=2)

        self.txt_click_delay = tk.Entry(self.window, width=7)
        self.txt_click_delay.grid(column=1, row=0)
        self.txt_click_delay.insert(0, '1000')

        self.random_delay = tk.Checkbutton(self.window, text='Random delay')
        self.random_delay.grid(column=2, row=0)

        self.btn_toggle_clicker = tk.Button(self.window, text='Start', command=self.toggle_clicker, font=("Arial", 12))
        self.btn_toggle_clicker.grid(column=2, row=2)

        self.random_delay.var = tk.BooleanVar()
        self.random_delay.config(variable=self.random_delay.var)
        self.clicker.random_delay = self.random_delay.var

        key.add_hotkey('space', self.toggle_clicker)

    def toggle_clicker(self):
        self.clicker.toggle_clicking()
        self.update_button_text()

    def update_button_text(self):
        if self.clicker.is_clicking:
            self.btn_toggle_clicker.config(text='Pause')
        else:
            self.btn_toggle_clicker.config(text='Start')

    def run(self):
        self.window.mainloop()


class JustClickerGUI(KeyClickerGUI):
    def __init__(self, clicker):
        super().__init__(clicker)
        self.window.title("JustClicker")
        self.window.geometry('360x170')

        self.lb_cycle_delay = tk.Label(self.window, text='Cycle delay (s):', font=("Arial Bold", 12))
        self.lb_save = tk.Label(self.window, text='Save coordinates:', font=("Arial", 12))
        self.lb_tab = tk.Label(self.window, text='Tab', font=("Arial", 12))

        self.lb_cycle_delay.grid(column=0, row=1)
        self.lb_save.grid(column=0, row=4)
        self.lb_tab.grid(column=1, row=4)

        self.txt_cycle_delay = tk.Entry(self.window, width=7)
        self.txt_cycle_delay.grid(column=1, row=1)
        self.txt_cycle_delay.insert(0, '60')

        self.status_label = tk.Label(self.window, text='', font=("Arial", 12), fg='green')
        self.status_label.grid(column=0, row=6, columnspan=3)

        self.cycle_timer_label = tk.Label(self.window, text='', font=("Arial Bold", 12), fg='red')
        self.cycle_timer_label.grid(column=2, row=1, columnspan=3)

        self.btn_reset = tk.Button(self.window, text='Reset Coordinates', command=self.clicker.reset_coordinates, font=("Arial", 12))
        self.btn_reset.grid(column=0, row=5)

        self.btn_save_file = tk.Button(self.window, text='Save crds', command=self.save_coordinates_to_file, font=("Arial Bold", 12))
        self.btn_save_file.grid(column=1, row=5)

        self.btn_load_file = tk.Button(self.window, text='Load crds', command=self.load_coordinates_from_file, font=("Arial Bold", 12))
        self.btn_load_file.grid(column=2, row=5)

        key.add_hotkey('tab', self.save_coordinates)

    def save_coordinates(self):
        x, y = self.clicker.add_current_position()
        self.status_label.config(text=f'Coordinates saved: ({x}, {y})')

    def save_coordinates_to_file(self):
        # Assuming self.clicker.coordinates is a list of tuples [(x1, y1), (x2, y2), ...]
        with open('coordinates.json', 'w') as file:
            json.dump(self.clicker.coordinates, file)
            self.status_label.config(text='Coordinates saved successfully.')

    def load_coordinates_from_file(self):
        try:
            with open('coordinates.json', 'r') as file:
                self.clicker.coordinates = json.load(file)
                self.status_label.config(text='Coordinates loaded successfully.')
        except FileNotFoundError:
            self.status_label.config(text='No saved coordinates file found.')


class ClickerSelection:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Select Clicker")
        self.window.geometry('300x100')

        self.lb_clicker_type = tk.Label(self.window, text='Select Clicker Type:', font=("Arial", 12))
        self.lb_clicker_type.grid(column=0, row=0)

        self.clicker_type = tk.StringVar()
        self.clicker_type.set('PyAutoGuiClicker')

        self.clicker_dropdown = ttk.Combobox(self.window, textvariable=self.clicker_type,
                                             values=['PyAutoGuiClicker', 'PynputClicker', 'KeyboardClicker'],
                                             state='readonly')
        self.clicker_dropdown.grid(column=1, row=0)
        self.clicker_dropdown.bind('<<ComboboxSelected>>', self.update_options)

        self.lb_option = tk.Label(self.window, text='Select Button:', font=("Arial", 12))
        self.lb_option.grid(column=0, row=1)

        self.option_frame = tk.Frame(self.window)
        self.option_frame.grid(column=1, row=1)

        self.key_entry = tk.Entry(self.option_frame, width=10)
        self.key_entry.grid(row=1, column=1)

        self.lb_key = tk.Label(self.option_frame, text='Key:', font=("Arial", 12))
        self.lb_key.grid(row=1, column=0)

        self.mouse_button_var = tk.StringVar()
        self.mouse_button_var.set('left')

        self.mouse_buttons = tk.Frame(self.option_frame)
        self.mouse_buttons.grid(row=2, column=0, columnspan=2)

        tk.Radiobutton(self.mouse_buttons, text='Left', variable=self.mouse_button_var, value='left').pack(side=tk.LEFT)
        tk.Radiobutton(self.mouse_buttons, text='Right', variable=self.mouse_button_var, value='right').pack(side=tk.RIGHT)

        self.btn_confirm = tk.Button(self.window, text='Confirm', command=self.confirm_selection, font=("Arial", 12))
        self.btn_confirm.grid(column=0, row=2, columnspan=2)

        self.update_options()

    def update_options(self, event=None):
        clicker_type = self.clicker_type.get()
        if clicker_type == 'KeyboardClicker':
            self.key_entry.grid(row=1, column=1)
            self.lb_key.grid(row=1, column=0)
            self.mouse_buttons.grid_forget()
        else:
            self.key_entry.grid_forget()
            self.lb_key.grid_forget()
            self.mouse_buttons.grid(row=2, column=0, columnspan=2)

    def confirm_selection(self):
        clicker_type = self.clicker_type.get()
        if clicker_type == 'PyAutoGuiClicker':
            clicker = clickers.PyAutoGuiClicker(btn_to_press=self.mouse_button_var.get())
            gui = JustClickerGUI(clicker)
        elif clicker_type == 'PynputClicker':
            if self.mouse_button_var.get()=='right':
                clicker = clickers.PynputClicker(btn_to_press=Button.right)
            else:
                clicker = clickers.PynputClicker(btn_to_press=Button.left)
            gui = JustClickerGUI(clicker)
        elif clicker_type == 'KeyboardClicker':
            key_to_press = self.key_entry.get()
            if key_to_press.isalpha() and len(key_to_press) == 1:
                clicker = clickers.KeyboardClicker(key_to_press)
            else:
                try:
                    clicker = clickers.KeyboardClicker(Key[key_to_press.lower()])
                except KeyError:
                    messagebox.showerror('Error', 'Invalid key selected.')
                    return
            gui = KeyClickerGUI(clicker)

        self.window.destroy()
        self.launch_main_gui(clicker, gui)


    def launch_main_gui(self, clicker, gui):
        start_click_thread(clicker, gui)
        gui.run()


def start_click_thread(clicker, gui):
    thread = threading.Thread(target=lambda: click_loop(clicker, gui))
    thread.daemon = True
    thread.start()


def click_loop(clicker, gui):
    while True:
        if clicker.is_clicking:
            try:
                t = float(gui.txt_click_delay.get()) / 1000
                clicker.click(t)
                if gui == JustClickerGUI:
                    for remaining in range(int(gui.txt_cycle_delay.get()), 0, -1):
                        if not clicker.is_clicking:
                            gui.cycle_timer_label.config(text="")
                            break
                        gui.cycle_timer_label.config(text=remaining)
                        time.sleep(1)
                    gui.cycle_timer_label.config(text='')
            except ValueError:
                messagebox.showerror('Error', 'Enter a valid Float value')
        time.sleep(0.001)



