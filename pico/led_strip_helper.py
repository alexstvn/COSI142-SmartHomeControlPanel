from machine import Pin
from utime import sleep, ticks_ms, ticks_diff
from ws2812 import WS2812

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

OFF = (0, 0, 0)

COLORS = {"BLACK": BLACK, "RED": RED, "YELLOW": YELLOW, "GREEN":GREEN, "CYAN":CYAN, "BLUE":BLUE, "PURPLE":PURPLE, "WHITE": WHITE}



def update_color(led, color):
    if color in COLORS:   
        led.pixels_fill(color)
        led.pixels_show()
        return
    else:
        print("Color: " + color + " is not in the list of colors")
        return

def light_on(led):
    led.pixels_fill(WHITE)
    led.pixels_show()

def light_off(led):
    led.pixels_fill(OFF)
    led.pixels_show()