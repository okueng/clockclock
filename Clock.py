import math

from Arduino import *
import platform
from tkinter import *
from threading import Timer
from math import cos, sin, pi
import PyCmdMessenger
from datetime import datetime, timedelta
from time import sleep

commands = [["moveClock1", "llllll"],
            ["moveClock2", "llllll"],
            ["setSpeed1", "ffffff"],
            ["setSpeed2", "ffffff"],
            ["setAccel1", "ffffff"],
            ["setAccel2", "ffffff"]]

modes = ["ANALOG", "DIGITAL","DIAGONAL","UP","MANUAL"]
coms = ["COM7","COM8","COM11","COM9"]

class Board:
    height = 3
    arduinos = []
    virtual_arduinos =[]
    handles = []
    extra_time = timedelta()
    last_animated = datetime.now()
    speed = 800
    accel = 800

    def init_handles(self, width: int, height: int) -> list:
        handles = []
        for x in range(0, width):
            for y in range(0, height):
                for z in range(0, 2):
                    handle = Handle(x, y, z)
                    handles.append(handle)
        return handles
    def set_speed_all(self):
        for arduino in self.arduinos:
            self.set_speed(arduino)

    def set_speed(self,cmd):
        sleep(0.05)
        cmd.send("setSpeed1",self.speed,self.speed,self.speed,self.speed,self.speed,self.speed)
        sleep(0.05)
        cmd.send("setSpeed2", self.speed, self.speed, self.speed, self.speed, self.speed, self.speed)
        sleep(0.05)
        cmd.send("setAccel1", self.accel, self.accel, self.accel, self.accel, self.accel, self.accel)
        sleep(0.05)
        cmd.send("setAccel2", self.accel, self.accel, self.accel, self.accel, self.accel, self.accel)
        sleep(0.05)

    def init_arduinos(self, width: int) -> list:
        arduinos = []
        for i in range(0, int(math.floor(width / 2))):
            port = "/dev/ttyACM" + str(i)
            if platform.system() == "Windows":
                port = coms[i]
            try:
                arduino = PyCmdMessenger.ArduinoBoard(port, baud_rate=57600)
                cmd = (PyCmdMessenger.CmdMessenger(arduino, commands))
                arduinos.append(cmd)
            except Exception as e:
                print(e)
            virtual_arduino = Arduino(i)
            self.virtual_arduinos.append(virtual_arduino)
        return arduinos

    def __init__(self,width=2):
        self.width = width
        self.last_cmd = None
        self.last_vrt_cmd = None
        self.handles = self.init_handles(self.width, self.height)
        self.arduinos = self.init_arduinos(self.width)
        self.set_speed_all()
        self.current_mode = 0

    def get_handle(self, x, y, z):
        return self.handles[x * 2 * self.height + y * 2 + z]

    def get_cmd(self,start_column=0):
        cmd = [self.get_handle(start_column+0, 0, 0).adjusted_angle(),
               self.get_handle(start_column+0, 0, 1).adjusted_angle(),
               self.get_handle(start_column+0, 1, 0).adjusted_angle(),
               self.get_handle(start_column+0, 1, 1).adjusted_angle(),
               self.get_handle(start_column+0, 2, 0).adjusted_angle(),
               self.get_handle(start_column+0, 2, 1).adjusted_angle(),
               self.get_handle(start_column+1, 0, 0).adjusted_angle(),
               self.get_handle(start_column+1, 0, 1).adjusted_angle(),
               self.get_handle(start_column+1, 1, 0).adjusted_angle(),
               self.get_handle(start_column+1, 1, 1).adjusted_angle(),
               self.get_handle(start_column+1, 2, 0).adjusted_angle(),
               self.get_handle(start_column+1, 2, 1).adjusted_angle()]
        return cmd

    def send_r(self,device,last_cmd):
        cmd = []
        for x in range(0,len(device)):
            cmd += self.get_cmd(x*2)
        if not (cmd == last_cmd):
            for x in range(0, len(device)):
                print("sending to device" + str(x) )
                try:
                    device[x].send("moveClock1",cmd[x*12 + 0],cmd[x*12 + 1],cmd[x*12 + 2],cmd[x*12 + 3],cmd[x*12 + 4],cmd[x*12 + 5])
                    sleep(0.05)
                    device[x].send("moveClock2",cmd[x*12 + 6],cmd[x*12 + 7],cmd[x*12 + 8],cmd[x*12 + 9],cmd[x*12 + 10],cmd[x*12 + 11])
                    sleep(0.05)
                except:
                    print("could not send :(")
        return cmd

    def send(self):
        #print("sending to virtual")
        self.last_vrt_cmd = self.send_r(self.virtual_arduinos,self.last_vrt_cmd)
        #print("sending to real")
        self.last_cmd =  self.send_r(self.arduinos,self.last_cmd)


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
        elif self.width == 6:
            self.set_digit(0, minute_first)
            self.set_digit(2, minute_second)
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
                      [1, 2, 0, 1, 0, 1, 3, 3, 2, 3, 0, 3],  # six
                      [1, 1, 3, 3, 3, 3, 3, 2, 2, 2, 0, 0],  # seven
                      [1, 2, 0, 1, 0, 1, 3, 2, 0, 3, 0, 3],  # height
                      [1, 2, 0, 1, 3, 3, 3, 2, 0, 2, 0, 0],  # nine
                      ]

        digits_2x3_alt = [[1, 2, 0, 2, 0, 1, 3, 2, 0, 2, 0, 3],  # zero
                      [2, 2, 0, 2, 0, 0, 1, 1, 1, 1, 1, 1],  # one
                      [1, 1, 1, 2, 0, 1, 3, 2, 0, 3, 3, 3],  # two
                      [1, 1, 1, 1, 1, 1, 3, 2, 0, 3, 0, 3],  # three
                      [2, 2, 0, 1, 3, 3, 2, 2, 0, 2, 0, 0],  # four
                      [1, 2, 0, 1, 1, 1, 3, 3, 3, 2, 0, 3],  # five
                      [1, 2, 0, 1, 0, 1, 3, 3, 2, 3, 0, 3],  # six
                      [1, 1, 3, 3, 3, 3, 3, 2, 2, 2, 0, 0],  # seven
                      [1, 2, 0, 1, 0, 1, 3, 2, 0, 3, 0, 3],  # height
                      [1, 2, 0, 1, 3, 3, 3, 2, 0, 2, 0, 0],  # nine
        ]

        glyph = digits_2x3[digit]
        if(start_row == 6):
            glyph = digits_2x3_alt[digit]


        for x in range(0, len(glyph)):
            gl = glyph[x] * 90
            self.handles[x+(start_row * 2 * self.height)].set_angle(gl)

    def set_analog_time(self):
        time = (datetime.now() + self.extra_time).time()
        hour_angle = math.floor(360.0 * (time.hour % 12) / 12.0)
        minute_angle = math.floor(360.0 * time.minute / 60.0)
        for x in range(0, self.width):
            for y in range(0, self.height):
                handle_hour = self.get_handle(x, y, 1)
                handle_hour.set_angle(hour_angle)
                handle_minute = self.get_handle(x, y, 0)
                handle_minute.set_angle(minute_angle)
    def set_diagonal(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                handle_hour = self.get_handle(x, y, 1)
                handle_hour.set_angle(45)
                handle_minute = self.get_handle(x, y, 0)
                handle_minute.set_angle(225)
    def set_up(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                handle_hour = self.get_handle(x, y, 1)
                handle_hour.set_angle(0)
                handle_minute = self.get_handle(x, y, 0)
                handle_minute.set_angle(0)
    def close(self):
        for arduino in self.arduinos:
            arduino.close()
            print("close")


    def key(self, event):
        if event.char == "a":
            self.extra_time += timedelta(minutes=1)
        elif event.char == "s":
            self.extra_time += timedelta(hours=1)
        elif event.char == "m":
            self.current_mode += 1
            if self.current_mode >= len(modes):
                self.current_mode = 0
        elif event.char == "c":
            self.close()
        elif event.char == "k":
            self.accel += 50
            self.speed += 50

            print("Accel" + str(self.accel))
            self.set_speed_all()
        elif event.char == "l":
            self.accel -= 50
            self.speed -= 50

            print("Accel" + str(self.accel))
            self.set_speed_all()
        else:
            index = int(event.char)
            self.current_mode = 4
            print(index)
            for x in range(0, self.width):
                for y in range(0, self.height):
                    handle_hour = self.get_handle(x, y, 1)
                    handle_hour.set_angle((45 * index)%360)
                    handle_minute = self.get_handle(x, y, 0)
                    handle_minute.set_angle((45 * index)%360)

    def run(self):
        now = datetime.now()
        # print(str((now - self.last_time).seconds))
        elapsed = now - self.last_animated
        if elapsed.microseconds > 900:
            self.last_animated = now
            if modes[self.current_mode] == "ANALOG":
                self.set_analog_time()
            elif modes[self.current_mode] == "DIGITAL":
                self.set_digital_time()
            elif modes[self.current_mode] == "DIAGONAL":
                self.set_diagonal()
            elif modes[self.current_mode] == "UP":
                self.set_up()
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
        self.current_angle = 90
        self.target_angle = 90
        self.type = z
    def set_angle(self,angle):
        self.previous_angle = self.target_angle
        self.target_angle = angle

    def adjusted_angle(self):
        new_angle = self.target_angle
        direction = self.target_angle-self.previous_angle
        if self.type == 1:
            if self.target_angle == 0:
                if direction > 0:
                    new_angle += 1
                else:
                    new_angle -= 1
            if 0 < self.target_angle <= 45:
                new_angle -= 1
            if 45 < self.target_angle <= 90:
                new_angle -= 1
            if 90 < self.target_angle <= 135:
                new_angle -= 2
            if 135 < self.target_angle < 180:
                new_angle -= 0
            if self.target_angle == 180:
                if direction > 0:
                    new_angle += 1
                else:
                    new_angle -= 2
            if 180 < self.target_angle <= 225:
                new_angle += 1
            if 225 < self.target_angle <= 270:
                new_angle += 1
            if 270 < self.target_angle <= 315:
                new_angle += 2
            if 315 < self.target_angle < 360:
                new_angle += 2
        return new_angle*4


def test():
    arduino = PyCmdMessenger.ArduinoBoard("COM11", baud_rate=57600)
    cmd = (PyCmdMessenger.CmdMessenger(arduino, commands))
    return cmd

def hop2(cmd,step1,step2):
    cmd.send("moveClock1",180*step1, 180 * step2, 0, 0, 0, 0)


b = Board(width=8)
b.run()

master = Tk()
master.bind("<Key>", b.key)
w = Canvas(master, width=b.width*200, height=600)
for arduino in b.virtual_arduinos:
    arduino.setCanvas(master, w)
    arduino.animate()
w.pack()
master.mainloop()
