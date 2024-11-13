from machine import Pin, I2C
from utime import sleep
from DHT20 import DHT20
from lcd1602 import LCD1602

# Initialize the I2C for the DHT20 sensor (I2C bus 0)
i2c0_sda = Pin(8)
i2c0_scl = Pin(9)
i2c0 = I2C(0, sda=i2c0_sda, scl=i2c0_scl)

# Initialize the DHT20 sensor
dht20 = DHT20(0x38, i2c0)

# Initialize the I2C for the LCD1602 display (I2C bus 1)
i2c1 = I2C(1, scl=Pin(7), sda=Pin(6), freq=400000)
d = LCD1602(i2c1, 2, 16)  # 2 rows, 16 characters per row

d.display()  # Start the display

while True:
    # Read temperature and humidity from the sensor
    measurements = dht20.measurements
    temperature = measurements['t']
    humidity = measurements['rh']
    
    # Clear the display and show the measurements
    d.clear()
    d.setCursor(0, 0)
    d.print(f"Temp: {temperature:.1f}C")
    d.setCursor(0, 1)
    d.print(f"Humid: {humidity:.1f}%")
    
    # Wait for 2 seconds before updating
    sleep(2)
