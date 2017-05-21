import math

from Arduino import *
import platform
from tkinter import *
from threading import Timer
from math import cos, sin, pi
import PyCmdMessenger
from datetime import datetime, timedelta

commands = [["moveClock1", "llllll"],
            ["moveClock2", "llllll"],
            ["setSpeed", "ffffffffffff"],
            ["setAccel", "ffffffffffff"]]


class Board:
    height = 3
    width = 4
    arduinos = []
    handles = []
    extra_time = timedelta()
    last_animated = datetime.now()

    def init_handles(self, width: int, height: int) -> list:
        handles = []
        for x in range(0, width):
            for y in range(0, height):
                for z in range(0, 2):
                    handle = Handle(x, y, z)
                    handles.append(handle)
        return handles

    def init_arduinos(self, width: int) -> list:
        arduinos = []
        for i in range(0, int(math.floor(width / 2))):
            port = "/dev/ttyACM" + str(i)
            if platform.system() == "Windows":
                port = "COM" + str(i + 7)
            try:
                arduino = PyCmdMessenger.ArduinoBoard(port, baud_rate=57600)
                cmd = (PyCmdMessenger.CmdMessenger(arduino, commands))
                arduinos.append(cmd)
            except Exception as e:
                print(e)
                a = Arduino(i)
                arduinos.append(a)
        return arduinos

    def __init__(self):
        self.last_cmd = None
        self.handles = self.init_handles(self.width, self.height)
        self.arduinos = self.init_arduinos(self.width)

    def get_handle(self, x, y, z):
        return self.handles[x * 2 * self.height + y * 2 + z]

    def get_cmd(self,start_column=0):
        cmd = [self.get_handle(start_column+0, 0, 0).target_angle,
               self.get_handle(start_column+0, 0, 1).target_angle,
               self.get_handle(start_column+0, 1, 0).target_angle,
               self.get_handle(start_column+0, 1, 1).target_angle,
               self.get_handle(start_column+0, 2, 0).target_angle,
               self.get_handle(start_column+0, 2, 1).target_angle,
               self.get_handle(start_column+1, 0, 0).target_angle,
               self.get_handle(start_column+1, 0, 1).target_angle,
               self.get_handle(start_column+1, 1, 0).target_angle,
               self.get_handle(start_column+1, 1, 1).target_angle,
               self.get_handle(start_column+1, 2, 0).target_angle,
               self.get_handle(start_column+1, 2, 1).target_angle]
        return cmd

    def send(self):
        cmd = []
        for x in range(0,len(self.arduinos)):
            cmd += self.get_cmd(x*2)
        if not (cmd == self.last_cmd):
            self.last_cmd = cmd
            for x in range(0, len(self.arduinos)):
                self.arduinos[x].send("moveClock1",cmd[x*12 + 0]*4,cmd[x*12 + 1]*4,cmd[x*12 + 2]*4,cmd[x*12 + 3]*4,cmd[x*12 + 4]*4,cmd[x*12 + 5]*4)
                self.arduinos[x].send("moveClock2",cmd[x*12 + 6]*4,cmd[x*12 + 7]*4,cmd[x*12 + 8]*4,cmd[x*12 + 9]*4,cmd[x*12 + 10]*4,cmd[x*12 + 11]*4)

    def set_digital_time(self):
        time = (datetime.now() + self.extra_time).time()
        second_second = int(format(time.second, "02")[0])
        minute_first = int(format(time.minute, "02")[0])
        minute_second = int(format(time.minute, "02")[1])
        hour_first = int(format(time.hour, "02")[0])
        hour_second = int(format(time.hour, "02")[1])
        if self.width == 2:
            self.set_digit(0, second_second)
        elif self.width == 4:
            self.set_digit(0, minute_first)
            self.set_digit(2, second_second)
        elif self.width == 8:
            self.set_digit(0, hour_first)
            self.set_digit(2, hour_second)
            self.set_digit(4, minute_first)
            self.set_digit(6, minute_second)

    def set_digit(self, start_row, digit):

        digits_2x3 = [[1, 2, 0, 2, 0, 1, 3, 2, 0, 2, 0, 3],  # zero
                      [3, 3, 3, 3, 3, 3, 2, 2, 0, 2, 0, 0],  # one
                      [1, 1, 1, 2, 0, 1, 3, 2, 0, 3, 3, 3],  # two
                      [1, 1, 1, 1, 1, 1, 3, 2, 0, 3, 0, 3],  # three
                      [2, 2, 0, 1, 3, 3, 2, 2, 0, 2, 0, 0],  # four
                      [1, 2, 0, 1, 1, 1, 3, 3, 3, 2, 0, 3],  # five
                      [1, 2, 0, 1, 0, 1, 3, 3, 0, 3, 3, 3],  # six
                      [1, 1, 1, 2, 0, 1, 3, 2, 3, 2, 0, 3],  # seven
                      [1, 2, 0, 1, 0, 1, 3, 2, 0, 3, 0, 3],  # height
                      [1, 2, 0, 1, 3, 3, 3, 2, 0, 2, 0, 0],  # nine
                      ]

        glyph = digits_2x3[digit]

        for x in range(0, len(glyph)):
            gl = glyph[x] * 90
            self.handles[x+(start_row * 2 * self.height)].target_angle = gl

    def set_analog_time(self):
        time = (datetime.now() + self.extra_time).time()
        hour_angle = math.floor(360.0 * (time.hour % 12) / 12.0)
        minute_angle = math.floor(360.0 * time.minute / 60.0)
        for x in range(0, 2):
            for y in range(0, 3):
                handle_hour = self.get_handle(x, y, 1)
                handle_hour.target_angle = hour_angle
                handle_minute = self.get_handle(x, y, 0)
                handle_minute.target_angle = minute_angle

    def run(self):
        now = datetime.now()
        # print(str((now - self.last_time).seconds))
        elapsed = now - self.last_animated
        if elapsed.microseconds > 900:
            self.last_animated = now
            self.set_digital_time()
            self.send()
        t = Timer(0.1, self.run)
        t.start()


class Handle:
    global_position = (0, 0)
    type = 0
    current_angle = 0
    target_angle = 0
    def __init__(self, x, y, z):
        self.global_position = (x, y)
        self.current_angle = 180
        self.target_angle = 180
        self.type = z

b = Board()
b.run()

master = Tk()
w = Canvas(master, width=800, height=600)
for arduino in b.arduinos:
    arduino.setCanvas(w)
    arduino.animate()
w.pack()
master.mainloop()
