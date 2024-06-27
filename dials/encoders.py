import adafruit_seesaw.seesaw
import adafruit_seesaw.rotaryio
from board import SCL, SDA
import busio


class Encoders:
    def __init__(self):
        i2c = busio.I2C(SCL, SDA)
        seesaw = adafruit_seesaw.seesaw.Seesaw(i2c, 0x49)
        self.encoders = [adafruit_seesaw.rotaryio.IncrementalEncoder(seesaw, n) for n in range(4)]
        self.last_positions = [-1, -1, -1, -1]

    def get_positions(self):
        return [encoder.position for encoder in self.encoders]

    def get_last_position(self, n):
        return self.last_positions[n]

    def set_last_position(self, n, pos):
        self.last_positions[n] = pos

    def set_position(self, n, pos):
        self.encoders[n].position = pos

if __name__ == '__main__':
    encoders = Encoders()
    while True:
        print(encoders.get_positions())
