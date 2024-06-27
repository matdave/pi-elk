import adafruit_seesaw.seesaw
import adafruit_seesaw.neopixel
from board import SCL, SDA
import busio
from rainbowio import colorwheel


class Pixels:
    def __init__(self):
        i2c = busio.I2C(SCL, SDA)
        seesaw = adafruit_seesaw.seesaw.Seesaw(i2c, 0x49)
        self.pixels = adafruit_seesaw.neopixel.NeoPixel(seesaw, 18, 4)
        self.pixels.brightness = 0.5  # set brightness to 50%
        self.colors = [0, 0, 0, 0]

    def set_pixel(self, n, color):
        self.pixels.__setitem__(n, colorwheel(color))

    def write(self, n):
        self.pixels.__setitem__(n, colorwheel(self.colors[n]))

    def get_pixels(self):
        return self.pixels

    def clear(self):
        self.pixels.fill(0)

    def set_brightness(self, brightness):
        self.pixels.brightness = brightness

    def get_brightness(self):
        return self.pixels.brightness

    def set_color(self, n, color):
        self.colors[n] = color

    def get_color(self, n):
        return self.colors[n]