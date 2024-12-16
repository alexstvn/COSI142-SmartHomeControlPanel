from machine import Pin
from utime import sleep, ticks_ms, ticks_diff
from utils import connect_wifi, send_data

# Initialize components
miniPir = Pin(18, Pin.IN)  # PIR sensor

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
        sleep(0.1)
    print(count)
    return count > 3  # Consider motion significant if detected >3 times

# Main loop
while True:
    motion_detected = detect_significant_motion(miniPir)  # Check for major motion
    
    # Format the data for the server
    motion_state = 1 if motion_detected else 0
    data = {
        'device_id': 'motion_sensor',
        'readings': {
            'motion': motion_state
        }
    }
    send_data('10.42.0.74', data)  # Replace with server's IP address

    # LED behavior based on motion state
    # if motion_detected:
        #print("Significant Motion Detected")
        # last_motion_time = ticks_ms()  # Update the time of the last motion

  #  else:
        # Check if the timeout has elapsed
    #    if ticks_diff(ticks_ms(), last_motion_time) > motion_timeout:
   #         print("No motion detected for over a minute")

    
    sleep(0.1)  # Small delay to avoid excessive polling
