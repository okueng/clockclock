from tkinter import *
from math import sin, cos, pi
from datetime import timedelta, datetime
import time
from threading import Thread
import PyCmdMessenger
import platform

clock_size = 100
width = 2
height = 3

due = [None] * (int(width / 2))

commands = [["moveClock1", "llllll"],
            ["moveClock2", "llllll"],
            ["setSpeed", "ffffffffffff"],
            ["setAccel", "ffffffffffff"]]

modes = ["ANALOG", "DIGITAL"]


class Board:
    current_mode = 0
    dues = []
    clocks = []
    clocks_matrix = []
    width = 0
    height = 0
    last_time = None
    last_animated = None
    extra_time = timedelta()
    last_cmd = []

    def index2pos(self, index: int):
        return (int(index / self.height), index % self.height)

    def pos2index(self, x: tuple):
        return x[0] * self.height + x[1]

    def __init__(self, width: int, height: int, canvas: Canvas):
        self.width = width
        self.height = height
        index = 0
        self.canvas = canvas
        self.clocks_matrix = [[0 for x in range(height)] for y in range(width)]
        self.last_time = datetime.now() - timedelta(minutes=15)
        self.last_animated = datetime.now()
        for i in range(0, int(width / 2)):
            cmd = None
            port = "/dev/ttyACM" + str(i)
            if platform.system() == "Windows":
                port = "COM" + str(i + 8)
            try:
                arduino = PyCmdMessenger.ArduinoBoard(port, baud_rate=57600)
                cmd = (PyCmdMessenger.CmdMessenger(arduino, commands))
            except Exception as e:
                print(e)
            self.dues.append(cmd)

        for i in range(0, width * height):
            pos = self.index2pos(i)
            c = Clock(pos)
            self.clocks.append(c)
            self.clocks_matrix[pos[0]][pos[1]] = c

    def set_analog_time(self):
        time = (datetime.now() + self.extra_time).time()
        self.set_all(time.hour, time.minute)

    def set_digital_time(self):
        time = (datetime.now() + self.extra_time).time()
        self.set_digit(0, int(format(time.minute, "02")[1]))
        # self.set_digit(2, int(format(time.hour, "02")[1]))
        # self.set_digit(4, int(format(time.minute, "02")[0]))
        # self.set_digit(6, int(format(time.minute, "02")[1]))
        # self.set_digit(6, int(format(time.minute, "02")[1]))

    def set_all(self, hours, minutes):
        for clock in self.clocks:
            clock.first_set_angle_target(int(360 * hours / 12) - 90)
            clock.second_set_angle_target(int(360 * minutes / 60) - 90)

    def set_digit(self, position, digit):
        # get all the clocks concerned
        clock_digit = [[self.clocks[self.pos2index((x, y))] for x in range(0 + position, 2 + position)] for y in
                       range(0, 3)]

        if digit == 0:
            clock_digit[0][0].first_set_angle_target(0)
            clock_digit[0][0].second_set_angle_target(90)
            clock_digit[0][1].first_set_angle_target(180)
            clock_digit[0][1].second_set_angle_target(90)
            clock_digit[1][0].first_set_angle_target(90)
            clock_digit[1][0].second_set_angle_target(-90)
            clock_digit[1][1].first_set_angle_target(90)
            clock_digit[1][1].second_set_angle_target(-90)
            clock_digit[2][0].first_set_angle_target(0)
            clock_digit[2][0].second_set_angle_target(-90)
            clock_digit[2][1].first_set_angle_target(180)
            clock_digit[2][1].second_set_angle_target(-90)
        elif digit == 1 and position == 0:
            clock_digit[0][0].first_set_angle_target(180)
            clock_digit[0][0].second_set_angle_target(180)
            clock_digit[0][1].first_set_angle_target(90)
            clock_digit[0][1].second_set_angle_target(90)
            clock_digit[1][0].first_set_angle_target(180)
            clock_digit[1][0].second_set_angle_target(180)
            clock_digit[1][1].first_set_angle_target(90)
            clock_digit[1][1].second_set_angle_target(-90)
            clock_digit[2][0].first_set_angle_target(180)
            clock_digit[2][0].second_set_angle_target(180)
            clock_digit[2][1].first_set_angle_target(-90)
            clock_digit[2][1].second_set_angle_target(-90)
        elif digit == 1 and position != 0:
            clock_digit[0][0].first_set_angle_target(180)
            clock_digit[0][0].second_set_angle_target(180)
            clock_digit[0][1].first_set_angle_target(90)
            clock_digit[0][1].second_set_angle_target(90)
            clock_digit[1][0].first_set_angle_target(180)
            clock_digit[1][0].second_set_angle_target(180)
            clock_digit[1][1].first_set_angle_target(90)
            clock_digit[1][1].second_set_angle_target(-90)
            clock_digit[2][0].first_set_angle_target(180)
            clock_digit[2][0].second_set_angle_target(180)
            clock_digit[2][1].first_set_angle_target(-90)
            clock_digit[2][1].second_set_angle_target(-90)
        elif digit == 2:
            clock_digit[0][0].first_set_angle_target(0)
            clock_digit[0][0].second_set_angle_target(0)
            clock_digit[0][1].first_set_angle_target(180)
            clock_digit[0][1].second_set_angle_target(90)
            clock_digit[1][0].first_set_angle_target(0)
            clock_digit[1][0].second_set_angle_target(90)
            clock_digit[1][1].first_set_angle_target(180)
            clock_digit[1][1].second_set_angle_target(-90)
            clock_digit[2][0].first_set_angle_target(-90)
            clock_digit[2][0].second_set_angle_target(0)
            clock_digit[2][1].first_set_angle_target(180)
            clock_digit[2][1].second_set_angle_target(180)
        elif digit == 3:
            clock_digit[0][0].first_set_angle_target(0)
            clock_digit[0][0].second_set_angle_target(0)
            clock_digit[0][1].first_set_angle_target(180)
            clock_digit[0][1].second_set_angle_target(90)
            clock_digit[1][0].first_set_angle_target(0)
            clock_digit[1][0].second_set_angle_target(0)
            clock_digit[1][1].first_set_angle_target(180)
            clock_digit[1][1].second_set_angle_target(-90)
            clock_digit[2][0].first_set_angle_target(0)
            clock_digit[2][0].second_set_angle_target(0)
            clock_digit[2][1].first_set_angle_target(-90)
            clock_digit[2][1].second_set_angle_target(180)
        elif digit == 4:
            clock_digit[0][0].first_set_angle_target(90)
            clock_digit[0][0].second_set_angle_target(90)
            clock_digit[0][1].first_set_angle_target(90)
            clock_digit[0][1].second_set_angle_target(90)
            clock_digit[1][0].first_set_angle_target(-90)
            clock_digit[1][0].second_set_angle_target(0)
            clock_digit[1][1].first_set_angle_target(180)
            clock_digit[1][1].second_set_angle_target(-90)
            clock_digit[2][0].first_set_angle_target(180)
            clock_digit[2][0].second_set_angle_target(180)
            clock_digit[2][1].first_set_angle_target(-90)
            clock_digit[2][1].second_set_angle_target(-90)
        elif digit == 5:
            clock_digit[0][0].first_set_angle_target(0)
            clock_digit[0][0].second_set_angle_target(90)
            clock_digit[0][1].first_set_angle_target(180)
            clock_digit[0][1].second_set_angle_target(180)
            clock_digit[1][0].first_set_angle_target(-90)
            clock_digit[1][0].second_set_angle_target(0)
            clock_digit[1][1].first_set_angle_target(180)
            clock_digit[1][1].second_set_angle_target(90)
            clock_digit[2][0].first_set_angle_target(0)
            clock_digit[2][0].second_set_angle_target(0)
            clock_digit[2][1].first_set_angle_target(180)
            clock_digit[2][1].second_set_angle_target(-90)
        elif digit == 6:
            clock_digit[0][0].first_set_angle_target(0)
            clock_digit[0][0].second_set_angle_target(90)
            clock_digit[0][1].first_set_angle_target(180)
            clock_digit[0][1].second_set_angle_target(180)
            clock_digit[1][0].first_set_angle_target(-90)
            clock_digit[1][0].second_set_angle_target(90)
            clock_digit[1][1].first_set_angle_target(180)
            clock_digit[1][1].second_set_angle_target(90)
            clock_digit[2][0].first_set_angle_target(0)
            clock_digit[2][0].second_set_angle_target(-90)
            clock_digit[2][1].first_set_angle_target(180)
            clock_digit[2][1].second_set_angle_target(-90)
        elif digit == 7:
            clock_digit[0][0].first_set_angle_target(0)
            clock_digit[0][0].second_set_angle_target(0)
            clock_digit[0][1].first_set_angle_target(180)
            clock_digit[0][1].second_set_angle_target(90)
            clock_digit[1][0].first_set_angle_target(180)
            clock_digit[1][0].second_set_angle_target(180)
            clock_digit[1][1].first_set_angle_target(-90)
            clock_digit[1][1].second_set_angle_target(90)
            clock_digit[2][0].first_set_angle_target(180)
            clock_digit[2][0].second_set_angle_target(180)
            clock_digit[2][1].first_set_angle_target(-90)
            clock_digit[2][1].second_set_angle_target(-90)
        elif digit == 8:
            clock_digit[0][0].first_set_angle_target(0)
            clock_digit[0][0].second_set_angle_target(90)
            clock_digit[0][1].first_set_angle_target(180)
            clock_digit[0][1].second_set_angle_target(90)
            clock_digit[1][0].first_set_angle_target(0)
            clock_digit[1][0].second_set_angle_target(-90)
            clock_digit[1][1].first_set_angle_target(180)
            clock_digit[1][1].second_set_angle_target(-90)
            clock_digit[2][0].first_set_angle_target(0)
            clock_digit[2][0].second_set_angle_target(-90)
            clock_digit[2][1].first_set_angle_target(180)
            clock_digit[2][1].second_set_angle_target(-90)
        elif digit == 9:
            clock_digit[0][0].first_set_angle_target(0)
            clock_digit[0][0].second_set_angle_target(90)
            clock_digit[0][1].first_set_angle_target(180)
            clock_digit[0][1].second_set_angle_target(90)
            clock_digit[1][0].first_set_angle_target(-90)
            clock_digit[1][0].second_set_angle_target(0)
            clock_digit[1][1].first_set_angle_target(180)
            clock_digit[1][1].second_set_angle_target(-90)
            clock_digit[2][0].first_set_angle_target(0)
            clock_digit[2][0].second_set_angle_target(0)
            clock_digit[2][1].first_set_angle_target(-90)
            clock_digit[2][1].second_set_angle_target(180)

            # set the position of each clock

    def send(self):
        cmd = [[0 for x in range(0, 12)] for y in range(int(width / 2))]

        for clock in self.clocks:
            due_index = int(clock.global_position[0] / 2)
            index = (clock.global_position[0] % 2) * self.height + clock.global_position[1]

            cmd[due_index][index * 2] = int(clock.first_handle_target)
            cmd[due_index][index * 2 + 1] = int(clock.second_handle_target)
        if cmd == self.last_cmd:
            return
        print("sending")
        self.last_cmd = cmd
        for d in range(0, len(self.dues)):
            try:
                if self.dues[d]:
                    self.dues[d].send("moveClock1", cmd[d][0], cmd[d][1], cmd[d][2], cmd[d][3], cmd[d][4], cmd[d][5])
                    self.dues[d].send("moveClock2", cmd[d][6], cmd[d][7], cmd[d][8], cmd[d][9], cmd[d][10], cmd[d][11])
                    print("sending " + str(cmd[d]))
            except Exception as e:
                print("not sending")
                print(e)

    def draw(self):
        # get all of the clocks from the first

        for clock in self.clocks:
            clock.draw(self.canvas)

    def animate(self):
        now = datetime.now()
        # print(str((now - self.last_time).seconds))
        elapsed = now - self.last_animated
        self.last_animated = now
        if elapsed.microseconds > 500:
            if modes[self.current_mode] == "ANALOG":
                self.set_analog_time()
            elif modes[self.current_mode] == "DIGITAL":
                self.set_digital_time()
            else:
                print("hop")

            self.canvas.delete("all")
            for clock in self.clocks:
                clock.animate(elapsed)
            self.draw()
        self.send()
        self.canvas.after(50, self.animate)

    def key(self, event):
        if event.char == "a":
            self.extra_time += timedelta(minutes=1)
        elif event.char == "s":
            self.extra_time += timedelta(hours=1)
        elif event.char == "m":
            self.current_mode += 1
            if self.current_mode >= len(modes):
                self.current_mode = 0
        else:
            index = int(event.char)
            # self.clocks[index].first_handle_target += 360
            self.clocks[index].second_handle_target += 360
        self.animate()


class Clock:
    global_position = (0, 0)
    first_handle_pos = 0
    first_handle_max_pos = 4 * 360
    first_handle_target = 0
    first_handle_initial = 0

    second_handle_pos = 0
    second_handle_max_pos = 4 * 360
    second_handle_target = 0

    def first_set_angle_target(self, degrees: int):
        self.first_handle_target = degrees / 360 * self.first_handle_max_pos

    def second_set_angle_target(self, degrees: int):
        self.second_handle_target = degrees / 360 * self.second_handle_max_pos

    def first_add_degrees(self, degrees: int):
        self.first_handle_pos = (self.first_handle_pos + degrees) % self.first_handle_max_pos

    def second_add_degrees(self, degrees: int):
        self.second_handle_pos = (self.second_handle_pos + degrees) % self.second_handle_max_pos

    def animate(self, elapsed):
        # how many ms since last update?
        # speed 50pos/s
        speed = 0.0005
        increment = (speed * elapsed.microseconds)
        dif = (self.first_handle_pos % self.first_handle_max_pos) - (
        self.first_handle_target % self.first_handle_max_pos)
        if (abs(dif) < increment):
            self.first_handle_pos = self.first_handle_target
        else:
            self.first_handle_pos = (increment + self.first_handle_pos) % self.first_handle_max_pos

        dif = (self.second_handle_pos % (self.second_handle_max_pos)) - (
        (self.second_handle_target) % (self.second_handle_max_pos))
        # print("hello " + str(dif) +  " " + str(increment))
        if (abs(dif) < increment):
            self.second_handle_pos = self.second_handle_target
        else:
            self.second_handle_pos = (increment + self.second_handle_pos) % (self.second_handle_max_pos)

    def angle(self, x: int, x_max: int):
        return (x / x_max) * 2 * pi

    def first_angle(self):
        return self.angle(self.first_handle_pos, self.first_handle_max_pos)

    def second_angle(self):
        return self.angle(self.second_handle_pos, self.second_handle_max_pos)

    def angle2localCanvas(self, angle, clock_size):
        return (cos(angle) * clock_size / 2, sin(angle) * clock_size / 2)

    def __init__(self, position: tuple):
        self.global_position = position

    def draw(self, w: Canvas):
        top_left_x = self.global_position[0] * clock_size
        top_left_y = self.global_position[1] * clock_size
        center_x = top_left_x + clock_size / 2
        center_y = top_left_y + clock_size / 2

        w.create_oval(top_left_x, top_left_y, top_left_x + clock_size, top_left_y + clock_size, fill="white")
        w.create_line(center_x, center_y,
                      center_x + self.angle2localCanvas(self.first_angle(), clock_size - 20)[0],
                      center_y + self.angle2localCanvas(self.first_angle(), clock_size - 20)[1],
                      width=8, fill="red")
        w.create_line(center_x, center_y,
                      center_x + self.angle2localCanvas(self.second_angle(), clock_size)[0],
                      center_y + self.angle2localCanvas(self.second_angle(), clock_size)[1],
                      width=8, fill="blue")


# create a board
master = Tk()
w = Canvas(master, width=width * clock_size, height=height * clock_size)
board = Board(width=width, height=height, canvas=w)

master.bind("<Key>", board.key)
w.pack()

board.animate()

master.mainloop()
# create 6 clocks and add them to the board

# board makes a fullcircle

# board assign random position

# board reset them to 0
