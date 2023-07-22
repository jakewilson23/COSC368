from tkinter import *
from tkinter.ttk import *

window = Tk()
data = StringVar()
data.set("Data to display")
label = Label(window, textvariable=data)
label.grid(row=0, column=0)
entry = Entry(window, textvariable=data)
entry.grid(row=1, column=0)
clear = Button(window, text="Clear", command=lambda: clear_data(data))
clear.grid(row=2, column=0)
s = Style()
s.configure('TButton', font='helvetica 24', foreground='green')
quit = Button(window, text="Quit", command=window.destroy)
quit.grid(row=3, column=0)


def clear_data(data_to_clear):
    data_to_clear.set("")
    return


window.mainloop()



