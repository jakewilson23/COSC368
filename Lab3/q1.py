import tkinter
from tkinter import *
import random
import time
import csv


class FittsLawTestUI(object):
    """A Fitts Law Test UI, The user must click the green rectangle as fast as possible.
    You must supply 4 parameters to the Class:
        name        a string of the users name
        distances   a list of ints representing distances between rectangles
        widths      a list of ints representing width of rectangles
        num_reps    an int determining how many times each distance/width is tested (must be an even number

    The time taken to click the green ractangle along with other relevant values are saved in a csv text file
    named fitts_law_test_ui_log.txt located in the same directory as the python file.
    The csv is formatted as such:
            [Name]  [distance]  [width]     [selection number]  [time(ms)]
        eg. Andy    256         32          1                   634.0
    The distances and widths given are randomised on runtime
    After all the tests have been completed the rectangles will turn red and will be un-clickable."""
    def __init__(self, name, distances, widths, num_reps):

        # Need to be specified by the user
        self.name = name
        self.distances = distances
        self.widths = widths

        self.window = Tk()
        self.window_width = 600
        self.window_height = 500
        self.test_canvas = Canvas(self.window, width=self.window_width, height=self.window_height)
        self.test_canvas.pack()
        self.file_out = None

        self.distance_count = IntVar(value=0)
        self.widths_count = IntVar(value=0)
        self.rep_count = IntVar(value=0)
        self.timer_start = DoubleVar(value=0.0)
        self.num_of_reps = num_reps  # this should always be an even number e.g. 2,4,6,8,10
        self.test_end = False

        self.bar_width = 0
        self.bar_distance = 0
        self.total_span = 0
        self.margin = 0

        self.target_rectangle = None
        self.inactive_rectangle = None
        self.target_rectangle_left = False  # True if target rectangle is left, false if target is right

    def run_test(self):
        self.file_out = open('fitts_law_test_ui_log.txt', 'w', newline='')
        self.randomize_test()
        self.draw_rectangles()

    def randomize_test(self):
        temp_dist = self.distances
        temp_width = self.widths
        random.shuffle(temp_dist)
        random.shuffle(temp_width)
        self.distances = temp_dist
        self.widths = temp_width
        return

    def change_target(self):
        if self.target_rectangle_left:
            self.target_rectangle_left = False
        else:
            self.target_rectangle_left = True
        return

    def calculate_measurements(self):
        self.bar_width = self.widths[self.widths_count.get()]
        self.bar_distance = self.distances[self.distance_count.get()]
        self.total_span = self.bar_distance + self.bar_width
        self.margin = (self.window_width - self.total_span) / 2
        return

    def draw_rectangles(self):
        self.calculate_measurements()
        if self.target_rectangle is None:
            self.inactive_rectangle = self.test_canvas.create_rectangle(self.margin, 0, self.margin + self.bar_width,
                                                                        self.window_height, fill="blue")
            self.target_rectangle = self.test_canvas.create_rectangle(self.margin + self.bar_distance, 0,
                                                                      self.margin + self.bar_width + self.bar_distance,
                                                                      self.window_height, tags="clickable",
                                                                      fill="green")
        else:
            if self.target_rectangle_left:  # target rectangle is the left one and needs to be green
                self.test_canvas.coords(self.target_rectangle, self.margin, 0, self.margin + self.bar_width,
                                        self.window_height)
                self.test_canvas.itemconfigure(self.target_rectangle, fill="green")
                self.test_canvas.coords(self.inactive_rectangle, self.margin + self.bar_distance, 0,
                                        self.margin + self.bar_width + self.bar_distance,
                                        self.window_height)
                self.test_canvas.itemconfigure(self.inactive_rectangle, fill="blue")

            else:  # Target is right rectangle, make it green
                self.test_canvas.coords(self.inactive_rectangle, self.margin, 0, self.margin + self.bar_width,
                                        self.window_height)
                self.test_canvas.itemconfigure(self.inactive_rectangle, fill="blue")
                self.test_canvas.coords(self.target_rectangle, self.margin + self.bar_distance, 0,
                                        self.margin + self.bar_width + self.bar_distance,
                                        self.window_height)
                self.test_canvas.itemconfigure(self.target_rectangle, fill="green")
        if self.test_end:
            self.test_canvas.itemconfigure(self.target_rectangle, fill='red')
            self.test_canvas.itemconfigure(self.inactive_rectangle, fill='red')
        else:
            self.test_canvas.tag_bind("clickable", "<ButtonPress-1>", self.check_button_press)
            self.timer_start.set(time.time())
        return

    def check_button_press(self, event):
        if self.test_end:
            return
        # Collect time to click button and output to csv file
        total_time = (time.time() - self.timer_start.get()) * 1000
        test_output = csv.writer(self.file_out, delimiter=",")
        test_output.writerow(
            {self.name + " " + str(self.bar_distance) + " " + str(self.bar_width) + " " + str(
                self.rep_count.get()) + " " + str(total_time)})

        if self.rep_count.get() == (self.num_of_reps - 1):  # on last rep need to change distance and/or width
            self.rep_count.set(0)
            if self.distance_count.get() == (len(self.distances) - 1):  # on last distance need to change width
                self.distance_count.set(0)
                if self.widths_count.get() == (len(self.widths) - 1):  # on last width and distance, test over
                    self.widths_count.set(0)
                    self.test_end = True
                else:
                    self.widths_count.set(self.widths_count.get() + 1)
            else:
                self.distance_count.set(self.distance_count.get() + 1)
        else:
            self.rep_count.set(self.rep_count.get() + 1)

        self.change_target()
        self.draw_rectangles()
        return


if __name__ == "__main__":
    name = 'testperson1'
    dist = [64, 128, 256, 512]
    widths = [8, 16, 32]
    num_reps = 2
    test = FittsLawTestUI(name, dist, widths, num_reps)

    test.run_test()

    test.window.mainloop()
