from tkinter import *

window = Tk()

scrollx = Scrollbar(window, orient=HORIZONTAL)
scrollx.pack(side=BOTTOM, fill=X)

scrolly = Scrollbar(window)
scrolly.pack(side=RIGHT, fill=Y)

text = Text(window, wrap=NONE,width=24, height=10,
            xscrollcommand=scrollx.set,
            yscrollcommand=scrolly.set)
text.pack()

text_to_enter = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do",
                 "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut",
                 "enim ad minim veniam, quis nostrud exercitation ullamco",
                 "laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure",
                 "dolor in reprehenderit in voluptate velit esse cillum dolore eu",
                 "fugiat nulla pariatur. Excepteur sint occaecat cupidatat non",
                 "proident, sunt in culpa qui officia deserunt mollit anim id est",
                 "laborum.",
                 "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do",
                 "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut",
                 "enim ad minim veniam, quis nostrud exercitation ullamco",
                 "laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure",
                 "dolor in reprehenderit in voluptate velit esse cillum dolore eu",
                 "fugiat nulla pariatur. Excepteur sint occaecat cupidatat non",
                 "proident, sunt in culpa qui officia deserunt mollit anim id est",
                 "laborum."]
for count, line in enumerate(text_to_enter):
    text.insert(str(float(count + 1)), line + "\n")

scrollx.config(command=text.xview)
scrolly.config(command=text.yview)

mainloop()
