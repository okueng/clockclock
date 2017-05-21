import platform
from tkinter import *
from threading import Timer
from math import cos,sin,pi
import PyCmdMessenger
from datetime import datetime

class Arduino:
    engines = []
    def __init__(self,index):
        self.width = 2
        self.global_index = index
        self.last_animated = datetime.now()
        for x in range(0,self.width):
            for y in range(0,3):
                for z in range(0,2):
                    engine = Engine(((self.width*self.global_index)+ x,y),z)
                    self.engines.append(engine)

    def setCanvas(self,w:Canvas):
        self.canvas = w

    def angle2localCanvas(self, angle, clock_size):
        return (cos(angle-pi/2) * clock_size / 2, sin(angle-pi/2) * clock_size / 2)
    def get_engine(self, x, y, z):
        xx = x+(self.width*self.global_index)
        return self.engines[xx*6+y*2+z]

    def send(self,name,cmd0,cmd1,cmd2,cmd3,cmd4,cmd5):
            if name == "moveClock1":
                self.get_engine(0, 0, 0).moveToDegrees(cmd0/4)
                self.get_engine(0, 0, 1).moveToDegrees(cmd1/4)
                self.get_engine(0, 1, 0).moveToDegrees(cmd2/4)
                self.get_engine(0, 1, 1).moveToDegrees(cmd3/4)
                self.get_engine(0, 2, 0).moveToDegrees(cmd4/4)
                self.get_engine(0, 2, 1).moveToDegrees(cmd5/4)
            elif name == "moveClock2":
                self.get_engine(1, 0, 0).moveToDegrees(cmd0/4)
                self.get_engine(1, 0, 1).moveToDegrees(cmd1/4)
                self.get_engine(1, 1, 0).moveToDegrees(cmd2/4)
                self.get_engine(1, 1, 1).moveToDegrees(cmd3/4)
                self.get_engine(1, 2, 0).moveToDegrees(cmd4/4)
                self.get_engine(1, 2, 1).moveToDegrees(cmd5/4)

    def draw(self):
        clock_size=200
        for engine in self.engines:
            top_left_x = engine.global_position[0] * clock_size
            top_left_y = engine.global_position[1] * clock_size
            center_x = top_left_x + clock_size / 2
            center_y = top_left_y + clock_size / 2

            handle_color = "red"
            handle_size= clock_size - 20

            if engine.handle_type == 0:
                self.canvas.create_oval(top_left_x, top_left_y, top_left_x + clock_size, top_left_y + clock_size, fill="white")
                handle_size = clock_size
                handle_color = "blue"

            pos = self.angle2localCanvas(engine.current_angle(), handle_size)
            self.canvas.create_line(center_x, center_y,
                          center_x + pos[0],
                          center_y + pos[1],
                          width=8, fill=handle_color)
    def animate(self):
        now = datetime.now()
        # print(str((now - self.last_time).seconds))
        elapsed = now - self.last_animated
        self.last_animated = now
        for engine in self.engines:
            engine.run(elapsed)
        self.draw()
        self.canvas.after(100, self.animate)

class Engine:
    global_position = (0,0)
    handle_type = 0
    target_position = 0
    current_position = 0
    max_position = 2000

    def __init__(self,global_position,z):
        self.global_position = global_position
        self.handle_type = z
    def current_angle(self):
        return (self.current_position/self.max_position) * 2 * pi
    def moveToDegrees(self,angle):
        self.target_position = (angle/360.0) * self.max_position
    def run(self,elapsed):
        if abs(self.current_position-self.target_position) < 30 :
            self.current_position = self.target_position
        else:
            self.current_position = (self.current_position+30)%self.max_position