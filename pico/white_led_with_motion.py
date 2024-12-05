from machine import Pin
from utime import sleep, ticks_ms, ticks_diff
from ws2812 import WS2812
from utils import connect_wifi, send_data, receive_data
from led_strip_helper import light_off, light_on, update_color

# Define LED colors
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


# Initialize components
miniPir = Pin(18, Pin.IN)  # PIR sensor
led = WS2812(16, 10)       # LED strip

initialMotion = False

# Timer variables
last_motion_time = ticks_ms()  # Record the time of the last detected motion
motion_timeout = 60000         # Timeout in milliseconds (1 minute)

# Connect to Wi-Fi
connect_wifi('test123', '12345678')

# Motion detection function
def detect_significant_motion(pir, duration=0.5):
    """Check for consistent motion for a specific duration."""
    count = 0
    for _ in range(int(duration / 0.1)):  # Sample every 0.1 seconds
        if pir.value() == 1:
            count += 1
        sleep(0.2) #sleep can be changed, but keeping it low to minimize delay between manual color changes.
    return count > 3  # Consider motion significant if detected >3 times

def update_light(cur_data):
    #set LED color to selected value from manual control dashboard
    if cur_data and 'lights_1' in cur_data:
            cur_color = cur_data['lights_1']['color']
            cur_status = cur_data['lights_1']['isOn']
            if cur_status == False: #turn off lights if "Off" button is selected in control dashboard.
                light_off(led)
            else:
                update_color(led, cur_color)    
    else:
        light_on(led)

# Main loop
while True:
        
    motion_detected = detect_significant_motion(miniPir)  # Check for major motion
    if motion_detected: initialMotion = True
    
    if not initialMotion:
        light_off(led)
        continue

    # Format the data for the server
    motion_state = 1 if motion_detected else 0
    data = {
        'device_id': 'motion_sensor',
        'readings': {
            'motion': motion_state
        }
    }
    send_data('10.42.0.53', data)  # Replace with server's IP address
    cur_data = receive_data('10.42.0.53')
    
    #checking that the data has been received properly.
    if cur_data:
        cur_data = cur_data.json()
    # LED behavior based on motion state
    if motion_detected:
        print("Significant Motion Detected")
        last_motion_time = ticks_ms()  # Update the time of the last motion

        # Set LEDs to selected color from manual control dashboard.
        update_light(cur_data)
    else:
        # Check if the timeout has elapsed
        if ticks_diff(ticks_ms(), last_motion_time) > motion_timeout:
            print("No motion detected for over a minute, turning off LEDs")

            # Turn off LEDs
            light_off(led)
        else:
            # If timeout hasn't elapsed, continue updating color.
            update_light(cur_data)
            


    sleep(0.1)  # Small delay to avoid excessive polling


