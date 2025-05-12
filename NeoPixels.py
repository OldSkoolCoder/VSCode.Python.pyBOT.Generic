import json
import time
# Only Uncomment if running on a raspberry Pi
#import board
#import neopixel
import random
import config
from GlobalFunctions import *

class NeoPixels:
    def __init__(self):

# Only Uncomment if running on a raspberry Pi
        # self.ORDER = neopixel.GRB
        # self.NoOfLEDS = 32
        # self.GPIOPinNo = board.D12

        self.HTMLColours = {}
        self.HTMLColoursFilename = config.DEFAULT_JSON_DIRECTORY + 'HTMLColours.json'
        self.HTMLColoursSchema= {
            "colours": 
                {}
        }

# Only Uncomment if running on a raspberry Pi
        # self.pixels = neopixel.NeoPixel(
        #     self.GPIOPinNo, self.NoOfLEDS, brightness=0.1, auto_write=False, pixel_order=self.ORDER
        # )

        # self.pixels.fill((0,0,0))
        # self.pixels.show()

    #-------------------------------------------------------------------------------------------------------------------------------
    def readHTMLColours(self):
        with open(self.HTMLColoursFilename, 'r') as file:
            self.HTMLColours = json.load(file)

    # def wheel(self, pos):
    #     # Input a value 0 to 255 to get a color value.
    #     # The colours are a transition r - g - b - back to r.
    #     if pos < 0 or pos > 255:
    #         r = g = b = 0
    #     elif pos < 85:
    #         r = int(pos * 3)
    #         g = int(255 - pos * 3)
    #         b = 0
    #     elif pos < 170:
    #         pos -= 85
    #         r = int(255 - pos * 3)
    #         g = 0
    #         b = int(pos * 3)
    #     else:
    #         pos -= 170
    #         r = 0
    #         g = int(pos * 3)
    #         b = int(255 - pos * 3)
    #     return (r, g, b) if self.ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


    # def rainbow_cycle(self, wait):
    #     for j in range(255):
    #         for i in range(self.NoOfLEDS):
    #             pixel_index = (i * 256 // self.NoOfLEDS) + j
    #             self.pixels[i] = wheel(pixel_index & 255)
    #         self.pixels.show()
    #         time.sleep(wait)

    def getHTMLColourRGB(self, HTMLColour):
        HTMLColour = HTMLColour.upper()
        if HTMLColour == "RANDOM":
            # NoOfColours = len(self.HTMLColours['colours'])
            # colourPickedIndex = random.randint(0,NoOfColours-1)
            # print(colourPickedIndex)
            HTMLColourName, HTMLColourRGB = random.choice(list(self.HTMLColours['colours'].items()))
            print(HTMLColourRGB, HTMLColourName)
            return HTMLColourRGB
            
        if HTMLColour in self.HTMLColours['colours']:
            return self.HTMLColours['colours'][HTMLColour]
        else:
            return "000000"

    def changeColour(self, HTMLColour):

        # pixels = neopixel.NeoPixel(
        #     self.GPIOPinNo, self.NoOfLEDS, brightness=0.1, auto_write=False, pixel_order=self.ORDER
        # )

        # self.pixels.fill((0,0,0))
        # self.pixels.show()

        RGB = self.getHTMLColourRGB(HTMLColour)
        # HTMLColour = HTMLColour.upper()
        # if HTMLColour in self.HTMLColours['colours']:
        #     RGB = self.HTMLColours['colours'][HTMLColour]
        # else:
        #     RGB = "000000"

        Red = int(RGB[0:2], base=16)
        Green = int(RGB[2:4], base=16)
        Blue = int(RGB[4:6], base=16)

        print(RGB[0:2],RGB[2:4],RGB[4:6])
        print(Red,Green,Blue)

        self.pixels.fill((Red, Green, Blue))
        #pixels.fill((0, 255, 0))
        self.pixels.show()

# while True:
#     # Comment this line out if you have RGBW/GRBW NeoPixels
#     pixels.fill((255, 0, 0))
#     # Uncomment this line if you have RGBW/GRBW NeoPixels
#     # pixels.fill((255, 0, 0, 0))
#     self.pixels.show()
#     time.sleep(1)

#     # Comment this line out if you have RGBW/GRBW NeoPixels
#     pixels.fill((0, 255, 0))
#     # Uncomment this line if you have RGBW/GRBW NeoPixels
#     # pixels.fill((0, 255, 0, 0))
#     pixels.show()
#     time.sleep(1)

#     # Comment this line out if you have RGBW/GRBW NeoPixels
#     pixels.fill((0, 0, 255))
#     # Uncomment this line if you have RGBW/GRBW NeoPixels
#     # pixels.fill((0, 0, 255, 0))
#     pixels.show()
#     time.sleep(1)

#     rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step
