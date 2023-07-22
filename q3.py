import tkinter
from tkinter import *

board = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']

window = Tk()


def clear_data(data_to_clear):
    data_to_clear.set("")
    return


def add_data(data_to_add_to, new_key):
    data_to_add_to.set(data_to_add_to.get() + new_key)
    return


data = StringVar()
label = Label(window, textvariable=data)

frame_keys = Frame(window, borderwidth=4, relief=RIDGE, pady=5, padx=5)

clear = Button(window, text="Clear", command=lambda: clear_data(data), padx=20)

frame_keys.pack(side=BOTTOM, pady=20, padx=20)
label.pack(side=LEFT, pady=(20,0), padx=30)
clear.pack(side=RIGHT, pady=(20,0), padx=30)

for key_row, key_set in enumerate(board):
    key_row_frame = Frame(frame_keys)
    key_row_frame.pack(side=TOP, pady=1, padx=1)
    for key_column, key in enumerate(key_set):
        button = Button(key_row_frame, text=key, width=3, pady=3, command=lambda x=key: add_data(data, x))
        button.grid(row=key_row, column=key_column)

mainloop()
