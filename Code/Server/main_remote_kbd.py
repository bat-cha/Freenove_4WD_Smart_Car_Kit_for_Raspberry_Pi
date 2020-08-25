from Motor import *
from Buzzer import *
from servo import *
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
HEAD_UP = 18
HEAD_DOWN = 32
HEAD_CENTER = 46
HEAD_LEFT = 31
HEAD_RIGHT = 33
ARM_UP = 21
ARM_DOWN = 35
ARM_TIGHT = 34
ARM_RELEASE = 36

remote_keyboard = InputDevice('/dev/input/event0')

if __name__ == '__main__':
    PWM=Motor()
    buzzer = Buzzer()
    servo = Servo()
    servo0=90
    servo1=90
    servo6=0
    servo7=90
    try:
        for event in remote_keyboard.read_loop():
            if event.type == ecodes.EV_KEY:
                if event.value == 0: # release stop
                    PWM.setMotorModel(0,0,0,0)
                    buzzer.run('0')
                    sdcount = 0
                elif event.value == 1: # press - start
                    print(categorize(event))
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
                    elif event.code == HEAD_UP:
                        servo1+=10
                        if servo1>=180:
                            servo1=180
                        servo.setServoPwm('1',servo1)
                    elif event.code == HEAD_DOWN:
                        servo1-=10
                        if servo1<=80:
                            servo1=80
                        servo.setServoPwm('1',servo1)
                    elif event.code == HEAD_LEFT:
                        servo0-=10
                        if servo0<=0:
                            servo0=0
                        servo.setServoPwm('0',servo0)
                    elif event.code == HEAD_RIGHT:
                        servo0+=10
                        if servo0>=180:
                            servo0=180
                        servo.setServoPwm('0',servo0)
                    elif event.code == HEAD_CENTER:
                        servo.setServoPwm('0',90)
                        servo.setServoPwm('1',90)
                    elif event.code == ARM_UP:
                        servo6+=5
                        if servo6>=180:
                            servo6=180
                        servo.setServoPwm('6',servo6)
                    elif event.code == ARM_DOWN:
                        servo6-=5
                        if servo6<=0:
                            servo6=0
                        servo.setServoPwm('6',servo6)
                    elif event.code == ARM_TIGHT:
                        servo7-=5
                        if servo7<=0:
                            servo7=0
                        servo.setServoPwm('7',servo7)
                    elif event.code == ARM_RELEASE:
                        servo7+=5
                        if servo7>=180:
                            servo7=180
                        servo.setServoPwm('7',servo7)
                    else:
                        print(categorize(event))
    except KeyboardInterrupt:
        print('interrupt')
