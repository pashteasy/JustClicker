import pyautogui as auto
import time
import keyboard as key
import random
from tkinter import *
from tkinter import messagebox

window = Tk()
window.title("JustClicker")
window.geometry('320x140')

lb1 = Label(window, text = 'Click interval (s):', font=("Arial Bold", 12),)
lb2 = Label(window, text = 'Hot key start/pause:', font=("Arial Bold", 12))
lb3 = Label(window, text = 'Exit clicker mode:', font=("Arial Bold", 12))
lb4 = Label(window, text = 'Space', font=("Arial Bold", 12))
lb5 = Label(window, text = 'Esc', font=("Arial Bold", 12))
lb1.grid(column=0, row=0 )
lb2.grid(column=0, row=1)
lb3.grid(column=0, row=2)
lb4.grid(column=1, row=1)
lb5.grid(column=1, row=2)

txt = Entry(window, width=7)
txt.grid(column=1, row=0)  

chk = Checkbutton(window, text='Random delay')
chk.grid(column=1, row=3)

def click(t):
    if chk.getboolean:
        t = t + random.uniform(0,t)
    time.sleep(t)     
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
                click(t)
    except ValueError:
        messagebox.showerror('Error', 'Enter a valid Float value')
    
        
btn = Button(window, text = 'Start', command=main, font=("Arial Bold", 12))
btn.grid(column=0, row=3) 
txt.focus()
isClicking = False
key.add_hotkey('space', set_clicker)

window.mainloop()



