import json
from this import d
from GlobalFunctions import *
import config
import threading
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

msgQueue = {}
inProgressMessage = {}

def messageScrolling(device, deviceNo):
    #global inProgressMessage

    while (len(msgQueue[deviceNo]) > 0 and not inProgressMessage[deviceNo]):
        msgText = msgQueue[deviceNo].pop(0)

        print(msgText)
        inProgressMessage[deviceNo] = True
        show_message(device, msgText, fill="white", font=proportional(LCD_FONT), scroll_delay=0.1)
        inProgressMessage[deviceNo] = False


class Matrix:
    def __init__(self, cascadeVal, deviceNo, ChipSelectNo):

        self.serial = spi(port=0, device=deviceNo, gpio_CS=ChipSelectNo, gpio=noop())
        self.device = max7219(self.serial, cascaded=cascadeVal, block_orientation=-90, rotate=2, contrast=1)
        self.deviceNo = deviceNo

        inProgressMessage[deviceNo] = False
        msgQueue[self.deviceNo] = []

        #show_message(self.device, "The Matrix is ONLINE", fill="white", font=proportional(LCD_FONT), scroll_delay=0.1)
        self.showMsg("The Matrix is ONLINE")

    def showMsg(self, text):
        #show_message(self.device, text, fill="white", font=proportional(LCD_FONT), scroll_delay=0.1)

        msgQueue[self.deviceNo].append(text)

        if not inProgressMessage[self.deviceNo]:
            thread = threading.Thread(target=messageScrolling, args=(self.device,self.deviceNo,))
            thread.start()

