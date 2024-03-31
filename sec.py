from tkinter import Tk, Button, Canvas
from time import time


window = Tk()
window.geometry('640x480')
window.title('Секундомер')
window.iconbitmap('secundant.ico')
window.resizable(width = False, height = False)
canvas = Canvas(window, width = 640, height = 480)
canvas.place(x = 0, y = 0, width = 640, height = 480)

def Reset():
    global time_text, restart_check

    restart_check = False
    canvas.delete('all')
    time_text = canvas.create_text(320, 50, text = '000:00:00:000', font = ('Arial', 25), width = 250)
    canvas.create_window((220,200), anchor = "nw", window = Button(text = 'Запустить', width = 10, font = ('Arial', 25), command = Start))
    
def Start():
    global check_timer_continue, start, but_stop

    start = time() - avg_time if restart_check else time()
    check_timer_continue = True 
    canvas.delete('all')
    but_stop = canvas.create_window((220, 200), anchor = "nw", window = Button(text = 'Остановить', width = 10, font = ('Arial', 25), command = End))
    Timer()

def End():
    global check_timer_continue, restart_check

    check_timer_continue = False
    restart_check = True
    canvas.delete(but_stop)
    canvas.create_window((220, 200), anchor = "nw", window = Button(text = 'Продолжить', width = 10, font = ('Arial', 25), command = Start))
    canvas.create_window((220, 275), anchor = 'nw', window = Button(text = 'Сбросить', width = 10, font = ('Arial', 25), command = Reset))

def Timer():
    global time_text, avg_time

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