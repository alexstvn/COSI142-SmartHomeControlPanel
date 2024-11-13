from ws2812 import WS2812
import time
from machine import Pin

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
COLORS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)

#WS2812(pin_num,led_count)
led = WS2812(16,15) #18,1
miniPir = Pin(18, Pin.IN)
cur_color = 0

while True:
    
    if miniPir.value()== 1:
        print('Motion Detected')
        led.pixels_fill(COLORS[cur_color])
        led.pixels_show()
        cur_color += 1
        cur_color %= len(COLORS)
        time.sleep(2)

print("fills")
for color in COLORS:
    led.pixels_fill(color)
    led.pixels_show()
    time.sleep(0.2)

print("chases")
for color in COLORS:
    led.color_chase(color, 0.01)

print("rainbow")
led.rainbow_cycle(0)


