import board
import neopixel
import time

class ledMatrice():
    def __init__(self):
        self.ledAmount = 256
        self.matricePin = board.D8
    def initMatrice(self):
        self.pixels = neopixel.NeoPixel(self.matricePin, self.ledAmount)

    def showMatrice(self):
        self.pixels.show()

    def fillMatrice(self, color):
        self.pixels.fill(color)

    def wheel(self, pos):
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.ledAmount):
                pixel_index = (i * 256 // self.ledAmount) + j
                self.pixels[i] = wheel(pixel_index & 255)
            self.pixels.show()
            time.sleep(wait)