import tkinter
from tkinter import *
import random
import time
import csv


class KeyboardTest(object):
    def __init__(self):
        self.window = Tk()
        self.name = None
        self.target_letters = None
        self.num_blocks = 0
        self.unique_letters = 6  # specified by the question
        self.blocks = []
        self.keyboard = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']  #Standard qwerty keyboard rows
        self.target_letter = StringVar()
        self.block_count = IntVar(value=0)
        self.letter_count = IntVar(value=0)
        self.timer_start = DoubleVar(value=0.0)
        self.frame_keys = None
        self.label = ""
        self.file_out = None
        self.test_type_dynamic = False
        self.test_type = ""

    def run_test(self):
        self.generate_random_target_letters()
        self.populate_blocks()
        if self.test_type_dynamic:
            self.file_out = open('experiment_dynamic_log.txt', 'w', newline='')
            self.test_type = "dynamic"
            self.build_keyboard()
            self.shuffle_keyboard()
        else:
            self.file_out = open('experiment_static_log.txt', 'w', newline='')
            self.test_type = "static"
            self.build_keyboard()
            self.shuffle_keyboard()

    def populate_blocks(self):
        for num in range(self.num_blocks):
            target_letters_list = list(self.target_letters)
            i = target_letters_list
            random.shuffle(i)
            self.blocks.append(i)

    def build_keyboard(self):
        self.target_letter.set("Press any Key to Begin")
        self.label = Label(self.window, textvariable=self.target_letter)
        self.frame_keys = Frame(self.window, borderwidth=4, relief=RIDGE, pady=5, padx=5)
        self.frame_keys.pack(side=BOTTOM, pady=20, padx=20)
        self.label.pack(side=TOP, pady=(20, 0), padx=30)

        # Put the Keys on the keyboard
        for key_row, key_set in enumerate(self.keyboard):
            key_row_frame = Frame(self.frame_keys)
            key_row_frame.pack(side=TOP, pady=1, padx=1)
            for key_column, key in enumerate(key_set):
                button_frame = Frame(key_row_frame, height=64, width=64)
                button_frame.pack_propagate(0)  # don't shrink
                button_frame.grid(row=key_row, column=key_column)
                button = Button(button_frame, text=key,
                                command=lambda x=key: self.increment_letter(x))
                button.pack(fill=BOTH, expand=1)

    def increment_letter(self, letter_clicked):
        if self.target_letter.get() == "Press any Key to Begin":  # Intro check only happens on launch
            self.target_letter.set(self.blocks[self.block_count.get()][self.letter_count.get()])
            self.timer_start.set(time.time())
            return
        elif not (letter_clicked == self.target_letter.get()):  # Incorrect click
            return
        else:
            # Collect time to click button and output to csv file
            total_time = (time.time() - self.timer_start.get()) * 1000
            test_output = csv.writer(self.file_out, delimiter=",")
            test_output.writerow(
                {self.name + " " + self.test_type + " " + self.target_letter.get() + " " + str(
                    self.block_count.get()) + " " +
                 str(total_time)})

            if self.letter_count.get() == (len(self.target_letters) - 1):  # last letter in block, revert back to 0
                self.letter_count.set(0)
                if self.block_count.get() == (self.num_blocks - 1):  # On the last Block and letter, Test Complete
                    self.target_letter.set("Complete")
                    return
                else:  # Not on last block, so increment it
                    self.block_count.set(self.block_count.get() + 1)
            else:  # Not on last letter, so increment it
                self.letter_count.set(self.letter_count.get() + 1)

            # get the next target and set timer
            self.target_letter.set(self.blocks[self.block_count.get()][self.letter_count.get()])
            if self.test_type_dynamic:  # If Dynamic Mode randomize the keyboard
                self.shuffle_keyboard()
            self.timer_start.set(time.time())
        return

    def shuffle_keyboard(self):
        temp_string = ""
        result = []
        for key_set in self.keyboard:
            temp_string += key_set
        t = list(temp_string)
        random.shuffle(t)

        # This is the number of keys on each row of a qwerty keyboard
        result.append(''.join(t[:10]))
        result.append(''.join(t[10:19]))
        result.append(''.join(t[19:26]))

        self.keyboard = result

        # Put the Keys on the keyboard
        self.frame_keys.pack_forget()
        self.frame_keys = Frame(self.window, borderwidth=4, relief=RIDGE, pady=5, padx=5)
        self.frame_keys.pack(side=BOTTOM, pady=20, padx=20)
        for key_row, key_set in enumerate(self.keyboard):
            key_row_frame = Frame(self.frame_keys)
            key_row_frame.pack(side=TOP, pady=1, padx=1)
            for key_column, key in enumerate(key_set):
                button_frame = Frame(key_row_frame, height=64, width=64)
                button_frame.pack_propagate(0)  # don't shrink
                button_frame.grid(row=key_row, column=key_column)
                button = Button(button_frame, text=key,
                                command=lambda x=key: self.increment_letter(x))
                button.pack(fill=BOTH, expand=1)

    def generate_random_target_letters(self):
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                    't', 'u', 'v', 'w', 'x', 'y', 'z']
        result = ''
        used_index = []
        while (len(used_index)) < self.unique_letters:
            rand_index = random.randint(0, (len(alphabet) - 1) - len(used_index))
            if rand_index not in used_index:
                result += alphabet[rand_index]
                used_index.append(rand_index)
        self.target_letters = result


if __name__ == "__main__":
    test = KeyboardTest()
    test.name = 'testperson'
    test.num_blocks = 6

    # either comment out or pass: test.test_type_dynamic = False to do a static test
    test.test_type_dynamic = True

    test.run_test()
    test.window.mainloop()
