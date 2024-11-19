from machine import Pin
from utime import sleep
from servo import SERVO
import time
from ws2812 import WS2812


BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
COLORS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)


servo = SERVO(Pin(20, Pin.OUT))
miniPir = Pin(18, Pin.IN)
led = WS2812(16,10)
# Initialize color index
color_index = 0

while True:
    if miniPir.value() == 1:
        print('Motion Detected')
        sleep(0.5)
        
        # Change to the next color in COLORS
        led.pixels_fill(COLORS[color_index])
        print("Color:", COLORS[color_index])
        led.pixels_show()
        
        # Update the color index for the next detection
        color_index = (color_index + 1) % len(COLORS)  # Cycle through COLORS
        
        sleep(0.5)
