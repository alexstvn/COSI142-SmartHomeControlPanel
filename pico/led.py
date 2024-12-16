import urequests
import time
from ws2812 import WS2812
from utils import connect_wifi

# Configuration
LED_PIN = 16  # GPIO pin connected to the LED strip (e.g., D16)
NUM_LEDS = 50  # Number of LEDs in the strip
SERVER_URL = "http://10.42.0.74:5000/led_state"  # Replace with the server's URL
FETCH_INTERVAL = 1  # Fetch interval in seconds

# Initialize LED strip
led = WS2812(LED_PIN, NUM_LEDS)

def set_led_color(color):
    """
    Set the LED strip to the given color.
    :param color: A hex color code string (e.g., "#FF0000").
    """
    # Convert hex color to RGB
    color = color.lstrip("#")
    red = int(color[0:2], 16)
    green = int(color[2:4], 16)
    blue = int(color[4:6], 16)

    # Update all LEDs with the color
    led.pixels_fill((red, green, blue))
    led.pixels_show()

def fetch_led_state():
    """
    Fetch the LED state from the server.
    :return: A dictionary with the LED state or None if the request fails.
    """
    try:
        response = urequests.get(SERVER_URL)
        if response.status_code == 200:
            led_state = response.json()
            response.close()
            return led_state
        else:
            print(f"Failed to fetch LED state: {response.status_code}")
            response.close()
            return None
    except Exception as e:
        print(f"Error fetching LED state: {e}")
        return None

def main():
    """
    Main loop to fetch the LED state and update the LED strip.
    """
    connect_wifi('test123', '12345678')
    while True:
        led_state = fetch_led_state()
        if led_state:
            # Check if the LED should be on
            if led_state.get("status") == 1:
                color = led_state.get("color", "#FFFFFF")  # Default to white
                set_led_color(color)
            else:
                # Turn off the LED strip
                set_led_color("#000000")
        else:
            print("No valid LED state received.")

        time.sleep(FETCH_INTERVAL)

# Run the main loop
main()
