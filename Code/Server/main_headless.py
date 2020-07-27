import io
import os
import socket
import struct
import time
import picamera
import sys
import getopt
from Thread import *
from threading import Thread
from server import Server
from Motor import *
from Buzzer import *
from evdev import InputDevice, categorize, ecodes

SPACE = 57
OK = 28
LEFT = 105
RIGHT = 106
UP = 103
DOWN = 108
VUP = 115
VDOWN = 114
PLAY = 164
PREV = 165
NEXT = 163
CONFIG = 171

remote_keyboard = InputDevice('/dev/input/event0')

class myserver():
    def __init__(self):
        self.TCP_Server = Server()
        self.TCP_Server.StartTcpServer()
        self.ReadData = Thread(target=self.TCP_Server.readdata)
        self.SendVideo = Thread(target=self.TCP_Server.sendvideo)
        self.power = Thread(target=self.TCP_Server.Power)
        self.SendVideo.start()
        self.ReadData.start()
        self.power.start()

    def close(self):
        try:
            stop_thread(self.SendVideo)
            stop_thread(self.ReadData)
            stop_thread(self.power)
        except:
            pass
        try:
            self.TCP_Server.server_socket.shutdown(2)
            self.TCP_Server.server_socket1.shutdown(2)
            self.TCP_Server.StopTcpServer()
        except:
            pass
        print("Close TCP")
        os._exit(0)


if __name__ == '__main__':
    myshow = myserver()
    PWM=Motor()
    buzzer = Buzzer()
    try:
        for event in remote_keyboard.read_loop():
            if event.type == ecodes.EV_KEY:
                if event.value == 0: # release stop
                    PWM.setMotorModel(0,0,0,0)
                    buzzer.run('0')
                    sdcount = 0
                elif event.value == 1: # press - start
                    if event.code == UP:
                        PWM.setMotorModel(1000,1000,1000,1000)      
                    elif event.code == DOWN:
                        PWM.setMotorModel(-1000,-1000,-1000,-1000)
                    elif event.code == LEFT:
                        PWM.setMotorModel(-1500,-1500,2000,2000)
                    elif event.code == RIGHT:
                        PWM.setMotorModel(2000,2000,-1500,-1500)
                    elif event.code == SPACE:
                        myshow.on_pushButton()
                    elif event.code == OK:
                        buzzer.run('1')
                    else:
                        print(categorize(event))
    except KeyboardInterrupt:
        myshow.close()
