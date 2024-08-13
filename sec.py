from tkinter import Tk, Button, Canvas
from time import time
from math import *


window = Tk()
window.geometry('640x480')
window.title('Секундомер')
window.iconbitmap('secundant.ico')
window.resizable(width = False, height = False)
canvas = Canvas(window, width = 640, height = 480)
canvas.place(x = 0, y = 0, width = 640, height = 480)
canvas_timers = Canvas()
up_down_check = False


def Reset():
    global time_text, restart_check, countdowns, countdowns_canvases,num_countdowns_canvas

    restart_check = False
    canvas.delete('all')
    canvas_timers.delete('all')
    num_countdowns_canvas = 0
    countdowns = countdowns_canvases = []
    time_text = canvas.create_text(320, 50, text = '000:00:00:000', font = ('Arial', 25), width = 250)
    canvas.create_window((220,125), anchor = "nw", window = Button(text = 'Запустить', width = 10, font = ('Arial', 25), command = Start))


def Countdown():
    global countdowns, countdowns_canvases, up_down_check

    if not up_down_check:
        countdowns.append(f'{len(countdowns) + 1}. {ts[0]}:{ts[1]}:{ts[2]}:{ts[3]}')
    countdowns_canvases = []
    number_countdowns_canvases = 0
    for i in range(ceil(len(countdowns) / 5)):
        countdowns_canvas = Canvas(window, width = 640, height = 205)
        end = number_countdowns_canvases * 5 + 5 if int(len(countdowns) / 5) > number_countdowns_canvases else len(countdowns)
        start = number_countdowns_canvases * 5

        for number_countdowns in range(start, end):
            countdowns_canvas.create_text(320, 25 + 25 * (number_countdowns - len(countdowns_canvases) * 5), text = countdowns[number_countdowns], font = ('Arial', 18), width = 250)
        countdowns_canvases.append(countdowns_canvas)
        number_countdowns_canvases += 1

    up_down_check = False
    Canvas_timers_placer()


def Canvas_timers_placer():
    global but_up, but_down, canvas_timers

    canvas.delete(but_up, but_down)
    canvas_timers.delete('all')
    canvas_timers = countdowns_canvases[num_countdowns_canvas]
    canvas_timers.place(x = 0, y = 275, width = 640, height = 205)

    if len(countdowns_canvases) > 1 and num_countdowns_canvas > 0:
        but_down = canvas.create_window((280, 450), window = Button(text = '<', width = 3, font = ('Arial', 15), command = Down))
    else:
        but_down = None

    if len(countdowns_canvases) > 1 and num_countdowns_canvas < len(countdowns_canvases) - 1:
        but_up = canvas.create_window((360, 450), window = Button(text = '>', width = 3, font = ('Arial', 15), command = Up))
    else:
        but_up = None


def Up():
    global num_countdowns_canvas, up_down_check
    num_countdowns_canvas += 1
    up_down_check = True
    Countdown()


def Down():
    global num_countdowns_canvas, up_down_check
    num_countdowns_canvas -= 1
    up_down_check = True
    Countdown()

    
def Start():
    global check_timer_continue, start, but_stop, but_countdown, but_up, but_down

    start = time() - avg_time if restart_check else time()
    check_timer_continue = True 
    canvas.delete('all')
    if len(countdowns_canvases) > 1 and num_countdowns_canvas > 0:
        but_down = canvas.create_window((280, 450), window = Button(text = '<', width = 3, font = ('Arial', 15), command = Down))
    else:
        but_down = None

    if len(countdowns_canvases) > 1 and num_countdowns_canvas < len(countdowns_canvases):
        but_up = canvas.create_window((360, 450), window = Button(text = '>', width = 3, font = ('Arial', 15), command = Up))
    else:
        but_up = None

    but_countdown = canvas.create_window((220, 125), anchor = "nw", window = Button(text = 'Отсчёт', width = 10, font = ('Arial', 25), command = Countdown))
    but_stop = canvas.create_window((220, 200), anchor = "nw", window = Button(text = 'Остановить', width = 10, font = ('Arial', 25), command = End))
    Timer()

def End():
    global check_timer_continue, restart_check, countdowns

    check_timer_continue = False
    restart_check = True
    canvas.delete(but_stop, but_countdown)
    canvas.create_window((220, 125), anchor = "nw", window = Button(text = 'Продолжить', width = 10, font = ('Arial', 25), command = Start))
    canvas.create_window((220, 200), anchor = 'nw', window = Button(text = 'Сбросить', width = 10, font = ('Arial', 25), command = Reset))

def Timer():
    global time_text, avg_time, ts

    avg_time = time() - start
    h = int(avg_time // 3600)
    m = int((avg_time - h * 3600) // 60)
    s = int(avg_time - h * 3600 - m * 60)
    ms = int((avg_time - h * 3600 - m * 60 - s) * 1000)
    ts = list(map(str, (h, m, s, ms)))

    for t in range(len(ts)):
        nuli = 3 if t == 3 or t == 0 else 2

        while len(ts[t]) < nuli:
            ts[t] = '0' + ts[t]

    canvas.delete(time_text)
    time_text = canvas.create_text(320, 50, text = f'{ts[0]}:{ts[1]}:{ts[2]}:{ts[3]}', font = ('Arial', 25), width = 250)

    if check_timer_continue:
        window.after(5, Timer)


Reset()

window.mainloop()