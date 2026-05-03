import time
from pca9685 import get_shared_pca9685


class Ordinary_Car:
    def __init__(self):
        # Shared with servo.py — single PCA9685 instance avoids the second
        # SLEEP→PRESCALE→WAKE transient on startup that briefly glitched the
        # servo PWM lines (audible trembling).
        self.pwm = get_shared_pca9685(address=0x40, freq=50)
    def duty_range(self, duty1, duty2, duty3, duty4):
        if duty1 > 4095:
            duty1 = 4095
        elif duty1 < -4095:
            duty1 = -4095        
        if duty2 > 4095:
            duty2 = 4095
        elif duty2 < -4095:
            duty2 = -4095  
        if duty3 > 4095:
            duty3 = 4095
        elif duty3 < -4095:
            duty3 = -4095
        if duty4 > 4095:
            duty4 = 4095
        elif duty4 < -4095:
            duty4 = -4095
        return duty1,duty2,duty3,duty4
    def left_upper_wheel(self,duty):
        if duty>0:
            self.pwm.set_motor_pwm(0,0)
            self.pwm.set_motor_pwm(1,duty)
        elif duty<0:
            self.pwm.set_motor_pwm(1,0)
            self.pwm.set_motor_pwm(0,abs(duty))
        else:
            self.pwm.set_motor_pwm(0,4095)
            self.pwm.set_motor_pwm(1,4095)
    def left_lower_wheel(self,duty):
        if duty>0:
            self.pwm.set_motor_pwm(3,0)
            self.pwm.set_motor_pwm(2,duty)
        elif duty<0:
            self.pwm.set_motor_pwm(2,0)
            self.pwm.set_motor_pwm(3,abs(duty))
        else:
            self.pwm.set_motor_pwm(2,4095)
            self.pwm.set_motor_pwm(3,4095)
    def right_upper_wheel(self,duty):
        if duty>0:
            self.pwm.set_motor_pwm(6,0)
            self.pwm.set_motor_pwm(7,duty)
        elif duty<0:
            self.pwm.set_motor_pwm(7,0)
            self.pwm.set_motor_pwm(6,abs(duty))
        else:
            self.pwm.set_motor_pwm(6,4095)
            self.pwm.set_motor_pwm(7,4095)
    def right_lower_wheel(self,duty):
        if duty>0:
            self.pwm.set_motor_pwm(4,0)
            self.pwm.set_motor_pwm(5,duty)
        elif duty<0:
            self.pwm.set_motor_pwm(5,0)
            self.pwm.set_motor_pwm(4,abs(duty))
        else:
            self.pwm.set_motor_pwm(4,4095)
            self.pwm.set_motor_pwm(5,4095)
    def set_motor_model(self, duty1, duty2, duty3, duty4):
        duty1,duty2,duty3,duty4=self.duty_range(duty1,duty2,duty3,duty4)
        # V1.0 chassis polarity: three of the four motor controllers are wired
        # such that "forward" wants the negated duty; only the right-lower
        # wheel takes the positive duty. Without this, e.g. left wheels spin
        # backwards when the iPhone Freenove app commands "forward".
        self.left_upper_wheel(-duty1)
        self.left_lower_wheel(-duty2)
        self.right_upper_wheel(-duty3)
        self.right_lower_wheel(duty4)

    def close(self):
        self.set_motor_model(0,0,0,0)
        # Don't close self.pwm — it's the process-shared PCA9685 instance.
        # The bus stays open for whatever else is using it (e.g. Servo).

if __name__=='__main__':
    PWM = Ordinary_Car()          
    try:
        PWM.set_motor_model(2000,2000,2000,2000)       #Forward
        time.sleep(1)
        PWM.set_motor_model(-2000,-2000,-2000,-2000)   #Back
        time.sleep(1)
        PWM.set_motor_model(-2000,-2000,2000,2000)     #Left 
        time.sleep(1)
        PWM.set_motor_model(2000,2000,-2000,-2000)     #Right    
        time.sleep(1)
        PWM.set_motor_model(0,0,0,0)                   #Stop
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        print ("\nEnd of program")
    finally:
        PWM.close()

