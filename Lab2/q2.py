"""Lab Aims
The aim of this lab is to further familiarise you with Graphical User Interface (GUI) programming with
Python/TkInter. The lab also introduces you to equipping software for cueing experimental tasks and logging user
interaction.

At the end of this lab you should understand the basics of the following:

cueing and logging experimental tasks for analysing user performance. Building the Experimental Interface In Lab 1
you developed a simple keyboard UI that allows text to be entered into a Label by pressing buttons. In this lab,
you will modify your program from Lab 1 to make an experimental interface.

The experimental interface will operate a bit differently: instead of entering text into the Label, the Label will be
used to tell the user which key to press (and will cycle through a series of letters). The keys themselves will be
laid out in one of two ways (detailed below).

You are encouraged to read through all the steps below before you begin rewriting your program so that you have a
clear understanding of the interface you are making.

Re-arrange the keyboard interface Make a new version of your keyboard program from Lab 1. Re-arrange the interface so
it looks similar to the screenshot below (ignore the letters on the keys for now):



Resize the Buttons Make sure that each button is square, with a width and height of around 64 pixels. Setting the
size of the button directly will not work (for a button containing text, the height and width arguments must be in
text units, not pixels), so instead you will need to put each button within its own frame. (Alternatively,
you could use the ipadx and ipady parameters to set the internal padding of the button when requesting its geometry
management with the "grid" geometry manager). You can then specify the size of the frame in pixels and use
pack_propagate to prevent the frame from shrinking. Here is an example that generates a single 64 x 64 button:

from tkinter import * from tkinter.ttk import * window = Tk() frame = Frame(window, height=64, width=64)
frame.pack_propagate(0) # don't shrink frame.grid(row=0, column=0) button = Button(frame, text="Hi") button.pack(
fill=BOTH, expand=1) window.mainloop() Cue a target letter and advance target on correct selection Create a variable
storing a string of target letters (e.g., 'abcdef'). Users will complete a set of n "blocks" (repetitions) of
selections. (Your program should store a value for n and decrement it after each block is completed. Eventually n
will be 6, but you may wish to use a lower number while you're developing your program.) Each block consists of one
selection of each of the target letters (each letter is randomly selected from the set of targets remaining in the
current block).

Once all targets have been selected for one block, the program should begin the next block. Once all blocks are
completed, the program should terminate (preferably showing a completion message to the user).

Use the Label widget to show the next target letter. After each correct Button press, the program should advance to
the next target.

Log the time taken to correctly select the item
Extend your program so it calculates the time (in milliseconds) from presentation of the cue to successful selection.

If you import the time package, the function call time.time() returns a floating point description of the current
clock time in seconds. The following code demonstrates how to calculate the total time (in milliseconds) to perform a
task:

     start = time.time()
     # perform whatever task you want to time
     total_time = (time.time() - start) * 1000

Write the selection time information to a log file, using the following format:

[Name] [condition] [target character] [block-count] [time taken to click key]

where the condition is static or dynamic (you will implement this next) and the block-count is the number of times
this character has been shown to the user. For example:

Andy static a 1 2468.0

The python csv module can be useful here (https://docs.python.org/3/library/csv.html#csv.writer).

Randomise the keyboard layout
Adding the following capabilities may require some re-engineering of your program.

In Lab 6 you will be using your keyboard UI to run some human factors experiments. These studies will involve
examining user performance in tasks involving visual search and spatial decisions. To facilitate these analyses your
keyboard UI should support two styles of use:

Static: which presents a randomized keyboard layout to users, but the keyboard remains static across selections.
Dynamic: which randomizes the location of every character key after every selection. Whether the program is running
in static or dynamic mode should be configurable using a variable. When running in static mode user events should be
written to the log file "experiment_static_log.txt”; and "experiment_dynamic_log.txt” when in dynamic mode.

Note that the Python module random includes a useful method shuffle that randomizes list content in place.

     import random
     some_list = ['a', 'b', 'c']
     random.shuffle(some_list)


Configure the target set The target set of characters (regardless of mode) used for the cueing mechanism implemented
above should comprise six blocks (repetitions) of the six randomly selected letters of the alphabet, using a random
order of letters in each block.

For example, when the program runs, the letters 'ahduef' may be randomly selected, and the six blocks may consist of
the following:

Block 1:  d, u, e, f, a, h

Block 2:  u, f, h, a, d, e

...

Block 6:  a, u, e, d, f, h
"""

import tkinter
from tkinter import *
import random
import time
import csv

board = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']
target_letters = 'abcdef'
num_blocks = 2
name = 'testperson1'

# Generate a number of shuffled target letters and put them in a list
# ie. 'abcdef' => [['e', 'f', 'a', 'd', 'b', 'c'], ['e', 'a', 'f', 'd', 'b', 'c']]
blocks = []
for num in range(num_blocks):
    target_letters_list = list(target_letters)
    i = target_letters_list
    random.shuffle(i)
    blocks.append(i)
print(blocks)

window = Tk()


def increment_letter(target, letter_clicked, current_block, current_letter, start_time, file_out):
    if target.get() == "Press any Key to Begin":    # Intro check only happens on launch
        target.set(blocks[block_count.get()][letter_count.get()])
        start_time.set(time.time())
        return
    elif not (letter_clicked == target.get()):  # Incorrect click
        return
    else:
        output_block = current_block.get()
        if current_letter.get() == (len(target_letters) - 1):  # last letter in block, revert letter back to 0
            current_letter.set(0)
            if current_block.get() == (num_blocks - 1):  # On the last Block and letter, Test Complete
                target.set("Complete")
                return
            else:   # Not on last block, so increment it
                current_block.set(current_block.get() + 1)
        else:   # Not on last letter, so increment it
            current_letter.set(current_letter.get() + 1)

        total_time = (time.time() - start_time.get()) * 1000
        test_output = csv.writer(file_out, delimiter=",")
        test_output.writerow({name + " " + 'static' + " " + target.get() + " " + str(output_block) + " " + str(total_time)})

        target.set(blocks[block_count.get()][letter_count.get()])
        start_time.set(time.time())
    return


target_letter = StringVar()
block_count = IntVar(value=0)
letter_count = IntVar(value=0)
timer_start = DoubleVar(value=0.0)
csvfile = open('experiment_static_log.txt', 'w', newline='')


target_letter.set("Press any Key to Begin")
label = Label(window, textvariable=target_letter)

frame_keys = Frame(window, borderwidth=4, relief=RIDGE, pady=5, padx=5)

frame_keys.pack(side=BOTTOM, pady=20, padx=20)
label.pack(side=TOP, pady=(20, 0), padx=30)

# Put the Keys on the keyboard
for key_row, key_set in enumerate(board):
    key_row_frame = Frame(frame_keys)
    key_row_frame.pack(side=TOP, pady=1, padx=1)
    for key_column, key in enumerate(key_set):
        button_frame = Frame(key_row_frame, height=64, width=64)
        button_frame.pack_propagate(0)  # don't shrink
        button_frame.grid(row=key_row, column=key_column)
        button = Button(button_frame, text=key,
                        command=lambda x=key: increment_letter(target_letter, x, block_count, letter_count,
                                                               timer_start, csvfile))
        button.pack(fill=BOTH, expand=1)

mainloop()
