from machine import Pin, I2C
from utime import sleep
from DHT20 import DHT20

from utils import connect_wifi, send_data

# Initialize the I2C for the DHT20 sensor (I2C bus 0)
i2c0_sda = Pin(8)
i2c0_scl = Pin(9)
i2c0 = I2C(0, sda=i2c0_sda, scl=i2c0_scl)

# Initialize the DHT20 sensor
dht20 = DHT20(0x38, i2c0)

connect_wifi('test123', '12345678')

while True:
    # Read temperature and humidity from the sensor
    measurements = dht20.measurements
    temperature = measurements['t']
    humidity = measurements['rh']

    data = {
        'device_id': 'temp_humidity_sensor',
        'readings':{
            'temperature': temperature,
            'humidity': humidity
        }
    }

    send_data('10.42.0.155', data)

    sleep(5)

