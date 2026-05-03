import threading

from pca9685 import get_shared_pca9685


# How long after each set_servo_pwm to keep the pulse alive before zeroing it.
# After this delay the servo loses holding torque (slight droop) but stops humming.
# 0.3s is enough for typical 50Hz hobby servos to physically reach the new angle.
SERVO_RELEASE_DELAY = 0.3


class Servo:
    def __init__(self):
        self.pwm_frequency = 50
        self.pwm_channel_map = {
            '0': 8,
            '1': 10,  # was 9; servo1 header is physically blocked on this chassis,
            '2': 10,  # tilt is wired to the servo2 header (PCA9685 ch 10).
            '3': 11,
            '4': 12,
            '5': 13,
            '6': 14,
            '7': 15
        }
        # Shared with motor.py — avoids a second SLEEP→PRESCALE→WAKE transient on startup,
        # which previously glitched the servo PWM lines and was audible as trembling.
        self.pwm_servo = get_shared_pca9685(address=0x40, freq=self.pwm_frequency)
        # NB: no startup pulse is sent to any channel. The OLD code initialised channels
        # 8+9 to 1500us; on this V1 chassis driving 1500us at startup made the servos
        # tremble and (with all 8 channels driven) heat up. We now leave channels at 0
        # until a real command lands — servos start limp and silent.
        self._release_timers = {}  # channel -> threading.Timer

    def angle_range(self, channel: str, angle: int) -> int:
        # Clamp commanded angle to the physical range each servo can hold without
        # grinding against an end stop. Pan (ch '0') and tilt (ch '1' → PCA9685 ch 10):
        # conservative 60-120. Other channels are unused on this chassis.
        if channel in ('0', '1', '2'):
            return max(60, min(120, angle))
        return angle

    def _release_channel(self, pwm_channel: int) -> None:
        # Zero the PWM duty so the servo stops receiving pulses → no holding torque,
        # no humming. Called from a Timer SERVO_RELEASE_DELAY after each move.
        self.pwm_servo.set_pwm(pwm_channel, 0, 0)

    def set_servo_pwm(self, channel: str, angle: int, error: int = 10) -> None:
        if channel not in self.pwm_channel_map:
            raise ValueError(
                f"Invalid channel: {channel}. Valid channels are {list(self.pwm_channel_map.keys())}.")
        angle = self.angle_range(channel, int(angle))
        pulse = 2500 - int((angle + error) / 0.09) if channel == '0' else 500 + int((angle + error) / 0.09)
        pwm_channel = self.pwm_channel_map[channel]
        self.pwm_servo.set_servo_pulse(pwm_channel, pulse)
        # Cancel any pending release for this channel and schedule a fresh one.
        existing = self._release_timers.get(pwm_channel)
        if existing is not None:
            existing.cancel()
        timer = threading.Timer(SERVO_RELEASE_DELAY, self._release_channel, args=(pwm_channel,))
        timer.daemon = True
        timer.start()
        self._release_timers[pwm_channel] = timer


# Main program logic follows:
if __name__ == '__main__':
    print("Now servos will rotate to 90 degree.")
    print("If they have already been at 90 degree, nothing will be observed.")
    print("Please keep the program running when installing the servos.")
    print("After that, you can press ctrl-C to end the program.")
    pwm_servo = Servo()
    try:
        while True:
            pwm_servo.set_servo_pwm('0', 90)
            pwm_servo.set_servo_pwm('1', 90)
    except KeyboardInterrupt:
        print("\nEnd of program")
