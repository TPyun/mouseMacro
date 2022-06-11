from tkinter import *
from tkinter.ttk import *

import pyautogui
import pyautogui as pg
import keyboard
import time

running = False
fixed = False
forever = True
set_time = 0
left_time = 0
start_time = 0

window = Tk()
window.title('CursorMaster')
window.geometry("+0+0")
window.resizable(False, False)


def Stop():
    global running
    running = False


state_frame = LabelFrame(labelanchor='n', text="Current state")
state_frame.pack(pady=5)
current_state = Label(state_frame)
current_state.pack()
show_left_time = Label(state_frame)
show_left_time.pack()


ChattingRoom_frame = LabelFrame(labelanchor='n', text="Current location")
ChattingRoom_frame.pack()
current_location = Label(ChattingRoom_frame)
current_location.pack(padx=50, pady=5)


def Show():
    global running
    rtext = '      Running!\nPress ESC to stop'
    stext = 'Sleeping'
    if running:
        current_state["text"] = rtext
    else:
        current_state["text"] = stext


Show()


def Fixed():
    global fixed
    fixed = True


def Free():
    global fixed
    fixed = False


def Forever():
    global forever
    forever = True


def Timer():
    global forever
    forever = False


radio_default = StringVar(value='auto')
setting_frame = LabelFrame(labelanchor='n', text="How long?")
setting_frame.pack(pady=5)
Radiobutton(setting_frame, text="Forever", value="auto", variable=radio_default, command=Forever).pack(side=LEFT)
Radiobutton(setting_frame, text="Direct input :", value="set", variable=radio_default, command=Timer).pack(side=LEFT)
ent = Entry(setting_frame, width=5)
ent.pack(side=LEFT)
Label(setting_frame, text='secs').pack()


move_radio_default = StringVar(value='move')
move_setting_frame = LabelFrame(labelanchor='n', text="Fixed?")
move_setting_frame.pack(pady=5)
Radiobutton(move_setting_frame, text="Move", value="move", variable=move_radio_default, command=Free).pack(side=LEFT)
Radiobutton(move_setting_frame, text="Fixed :", value="set", variable=move_radio_default, command=Fixed).pack(side=RIGHT)

current_x, current_y = pg.position()


def catchLocation():
    global current_x
    global current_y
    current_x, current_y = pg.position()
    location = f'{current_x}, {current_y}'
    current_location["text"] = location


def Press():
    pyautogui.click(x=current_x, y=current_y)


t = 0


def Time():
    global t
    t = t+1
    if running:
        window.after(1000, Time)


i = 0


def loop():
    global set_time
    global i
    global running
    global left_time
    global start_time
    global t

    if keyboard.is_pressed('shift'):
        running = True
    if keyboard.is_pressed('Escape'):
        running = False
        i = 0
        Show()
    if running:
        Press()
        i += 1
        window.after(10, Show)
        if not forever:
            if i == 1:
                set_time = int(ent.get()) + time.time()
                start_time = time.time()
                left_time = set_time - start_time
            if left_time <= 0:
                running = False
                left_time = 0
            start_time = time.time()
            left_time = set_time - start_time
            show_left_time['text'] = f'\nLeft time: {round(left_time)}'

    if running is False:
        catchLocation()
        i = 0
        t = 0
        left_time = 0
    if running is True and fixed is False:
        catchLocation()
    window.after(10, loop)


window.after(10, loop)

command_frame = LabelFrame(labelanchor='n')
command_frame.pack(fill=BOTH, padx=100)

window.mainloop()

