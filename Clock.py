import math

from Arduino import *
import platform
from tkinter import *
from threading import Timer
from math import cos,sin,pi
import PyCmdMessenger
from datetime import datetime,timedelta

commands = [["moveClock1", "llllll"],
            ["moveClock2", "llllll"],
            ["setSpeed", "ffffffffffff"],
            ["setAccel", "ffffffffffff"]]


class Board:
    arduinos = []
    handles = []
    extra_time =  timedelta()

    last_animated = datetime.now()
    hop = 0
    def __init__(self):
        width = 2
        for x in range(0,2):
            for y in range(0,3):
                for z in range(0,2):
                    handle = Handle(x,y,z)
                    self.handles.append(handle)

        for i in range(0, int(width / 2)):
            cmd = None
            port = "/dev/ttyACM" + str(i)
            if platform.system() == "Windows":
                port = "COM" + str(i + 8)
            try:
                arduino = PyCmdMessenger.ArduinoBoard(port, baud_rate=57600)
                cmd = (PyCmdMessenger.CmdMessenger(arduino, commands))
                self.arduinos.append(arduino)
            except Exception as e:
                print(e)
        if not self.arduinos:
            a = Arduino()
            self.arduinos.append(a)
    def get_handle(self,x,y,z):
        return self.handles[x*6 + y*2 + z]

    def send(self):
        for arduino in self.arduinos:
            arduino.send("moveClock1",
                         self.get_handle(0, 0, 0).target_angle,
                         self.get_handle(0, 0, 1).target_angle,
                         self.get_handle(0, 1, 0).target_angle,
                         self.get_handle(0, 1, 1).target_angle,
                         self.get_handle(0 ,2 ,0).target_angle,
                         self.get_handle(0 ,2 ,1).target_angle)
            arduino.send("moveClock2",
                         self.get_handle(1, 0, 0).target_angle,
                         self.get_handle(1, 0, 1).target_angle,
                         self.get_handle(1, 1, 0).target_angle,
                         self.get_handle(1, 1, 1).target_angle,
                         self.get_handle(1 ,2 ,0).target_angle,
                         self.get_handle(1 ,2 ,1).target_angle)
    def set_digital_time(self):
        pass
    def set_analog_time(self):
        time = (datetime.now() + self.extra_time).time()
        hour_angle = math.floor(360.0 * (time.hour%12) / 12.0)
        minute_angle = math.floor(360.0 * time.minute / 60.0)
        for x in range(0,2):
            for y in range(0,3):
                handle_hour = self.get_handle(x , y ,1)
                handle_hour.target_angle = hour_angle
                handle_minute = self.get_handle(x, y, 0)
                handle_minute.target_angle = minute_angle

    def run(self):
        now = datetime.now()
        # print(str((now - self.last_time).seconds))
        elapsed = now - self.last_animated
        if elapsed.microseconds > 500 :
            self.last_animated = now
            self.set_analog_time()
            self.send()
        t=Timer(0.5,self.run)
        t.start()


class Handle:
    global_position = (0,0)
    type = 0
    current_angle = 0
    target_angle = 0

    def __init__(self,x,y,z):
        self.global_position = (x,y)
        self.type = z




b = Board()
b.run()

master = Tk()
w = Canvas(master, width=400, height=600)
for arduino in b.arduinos:
    arduino.setCanvas(w)
    arduino.animate()
w.pack()
master.mainloop()


