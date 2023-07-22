import tkinter as tk  # Avoid `import *`

klavesnice = tk.Tk()
klavesnice.geometry("800x700+120+100")

buttons = [
    'q','w','e','r','t','y','u','i','o','p',
    'a','s','d','f','g','h','j','k','l',
    'z','x','c','v','b','n','m'
]

zadane = ''
entry = tk.Text(klavesnice, width=43, height=3)
entry.grid(row=1, columnspan=40)

def select(value):
    global zadane
    if value == 'Space':
        entry.insert('end', ' ')
    else:
        entry.insert('end', value)
        zadane = zadane + value
        print(f'{zadane=!r}')


radek = 3 #row
sloupec = 0 #column

for button in buttons:
    command = lambda x=button: select(x)
    if button != 'Space':
        tk.Button(klavesnice, text=button, width=5, font=("arial", 14, "bold"),
                  bg='powder blue', command=command, padx=3.5, pady=3.5, bd=5
                 ).grid(row=radek, column=sloupec)
    if button == 'Space':
        tk.Button(klavesnice, text=button, command=command).grid(row=5, column=sloupec)
    sloupec += 1
    # Specify the keyboard layout
    if sloupec > 9 and radek == 3:
        sloupec = 0
        radek += 1
    if sloupec > 8 and radek == 4:
        sloupec = 0
        radek += 1

klavesnice.mainloop()

