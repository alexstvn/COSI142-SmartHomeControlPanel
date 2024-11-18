# this will activate white LED strips when a motion has been detected, and the lights turn off if the motion sensor does not detect anything for over a minute
# continuous while loop, so the sensor works non-stop
from machine import Pin
from utime import sleep, ticks_ms, ticks_diff
from ws2812 import WS2812

# Define LED colors
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

# Initialize components
miniPir = Pin(18, Pin.IN)  # PIR sensor
led = WS2812(16, 10)       # LED strip

# Timer variables
last_motion_time = ticks_ms()  # Record the time of the last detected motion
motion_timeout = 60000         # Timeout in milliseconds (1 minute)

# Motion detection function
def detect_significant_motion(pir, duration=0.5):
    """Check for consistent motion for a specific duration."""
    count = 0
    for _ in range(int(duration / 0.1)):  # Sample every 0.1 seconds
        if pir.value() == 1:
            count += 1
        sleep(0.1)
    return count > 3  # Consider motion significant if detected >3 times

while True:
    if detect_significant_motion(miniPir):  # Check for major motion
        print("Significant Motion Detected")
        last_motion_time = ticks_ms()  # Update the time of the last motion
        
        # Set LEDs to white
        led.pixels_fill(WHITE)
        led.pixels_show()
    else:
        # Check if the timeout has elapsed
        if ticks_diff(ticks_ms(), last_motion_time) > motion_timeout:
            print("No motion detected for over a minute, turning off LEDs")
            
            # Turn off LEDs
            led.pixels_fill(OFF)
            led.pixels_show()
    
    sleep(0.1)  # Small delay to avoid excessive polling

