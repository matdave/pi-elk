from board import SCL, SDA, D4
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1305


class Display:
    def __init__(self):
        oled_reset = digitalio.DigitalInOut(D4)
        i2c = busio.I2C(SCL, SDA)
        self.disp = adafruit_ssd1305.SSD1305_I2C(128, 32, i2c, addr=0x3C, reset=oled_reset)
        self.disp.rotation = 2
        self.image = Image.new("1", (self.disp.width, self.disp.height))
        self.draw = ImageDraw.Draw(self.image)
        self.text = ['', '', '', '']

    def write(self, text1='', text2='', text3='', text4=''):
        if text1 == '':
            text1 = self.text[0]
        else:
            self.text[0] = text1
        if text2 == '':
            text2 = self.text[1]
        else:
            self.text[1] = text2
        if text3 == '':
            text3 = self.text[2]
        else:
            self.text[2] = text3
        if text4 == '':
            text4 = self.text[3]
        else:
            self.text[3] = text4

        font = ImageFont.load_default()
        x = 0
        top = -2
        self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)
        self.draw.text((x, top + 0), text1, font=font, fill=255)
        self.draw.text((x, top + 8), text2, font=font, fill=255)
        self.draw.text((x, top + 16), text3, font=font, fill=255)
        self.draw.text((x, top + 25), text4, font=font, fill=255)
        # Display image.
        self.disp.image(self.image)
        self.disp.show()

    def clear(self):
        self.set_text(0, '')
        self.set_text(1, '')
        self.set_text(2, '')
        self.set_text(3, '')
        self.write()
        self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)
        self.disp.image(self.image)
        self.disp.show()

    def set_text(self, n, text):
        self.text[n] = text


if __name__ == "__main__":
    display = Display()
    display.write("1", "2", "3", "4")
