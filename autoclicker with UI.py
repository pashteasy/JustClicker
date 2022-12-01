import pyautogui as auto
import time
import keyboard as key
from tkinter import *
from tkinter import messagebox

#окно
window = Tk()
window.title("Autoclicker by pashtzt")
window.geometry('320x140')
#текст 
lb1 = Label(window, text = 'Интервал нажатия (c):', font=("Arial Bold", 12),)
lb2 = Label(window, text = 'Старт и пауза:', font=("Arial Bold", 12))
lb3 = Label(window, text = 'Выйти из режима кликера:', font=("Arial Bold", 12))
lb4 = Label(window, text = 'Space', font=("Arial Bold", 12))
lb5 = Label(window, text = 'Esc', font=("Arial Bold", 12))
lb1.grid(column=0, row=0 )
lb2.grid(column=0, row=1)
lb3.grid(column=0, row=2)
lb4.grid(column=1, row=1)
lb5.grid(column=1, row=2)
#выбор задержки
txt = Entry(window, width=7)
txt.grid(column=1, row=0)  

def click(t): 
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
        messagebox.showerror('Ошибка', 'Введите корректное значение типа Float')
    
        
btn = Button(window, text = 'Запустить', command=main, font=("Arial Bold", 12))
btn.grid(column=0, row=3) 
txt.focus()
isClicking = False
key.add_hotkey('space', set_clicker)

window.mainloop()



