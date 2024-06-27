import adafruit_seesaw.seesaw
import adafruit_seesaw.digitalio
from board import SCL, SDA
import busio
import digitalio


class Switches:
    def __init__(self):
        i2c = busio.I2C(SCL, SDA)
        seesaw = adafruit_seesaw.seesaw.Seesaw(i2c, 0x49)
        self.switches = [adafruit_seesaw.digitalio.DigitalIO(seesaw, pin) for pin in (12, 14, 17, 9)]
        for switch in self.switches:
            switch.switch_to_input(digitalio.Pull.UP)  # input & pullup!
        self.last_positions = [True, True, True, True]

    def get_switches(self):
        return self.switches

    def get_switch(self, n):
        return self.get_switches()[n].value

    def get_last_position(self, n):
        return self.last_positions[n]

    def set_last_position(self, n, pos):
        self.last_positions[n] = pos

if __name__ == '__main__':
    switches = Switches()
    while True:
        print(switches.get_switch(0), switches.get_switch(1), switches.get_switch(2), switches.get_switch(3))