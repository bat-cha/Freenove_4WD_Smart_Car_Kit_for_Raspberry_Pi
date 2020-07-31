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
    try:
       pass
    except KeyboardInterrupt:
        myshow.close()
