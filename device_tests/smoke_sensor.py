# plug the pins in the following order:
# GND - pin 6, VCC - pin 2, SDA - pin 3, SCL - pin 5
# direct connection to raspberry pi, not through pico

from smbus2 import SMBus, i2c_msg
import time

HM3301_I2C_ADDR_WRITE = 0x80  # I2C write address
HM3301_I2C_ADDR_READ = 0x81   # I2C read address
DATA_CNT = 29                 # Total number of bytes expected in response

class HM3301Sensor:
    def __init__(self, bus_nr=1):
        self.bus_nr = bus_nr
        self.smbus = SMBus(bus_nr)
        self.init_sensor()

    def init_sensor(self):
        # Send the initialization command to enable I2C mode (0x88 to 0x80)
        try:
            init_command = [0x88]  # Command to switch to I2C mode
            write = i2c_msg.write(HM3301_I2C_ADDR_WRITE >> 1, init_command)
            self.smbus.i2c_rdwr(write)
            print("Initialization command sent successfully.")
        except Exception as e:
            print(f"Initialization failed: {e}")
        time.sleep(0.5)  # Wait for sensor to process the command

    def read_data(self):
        # Attempt to read 29 bytes of data from the sensor
        try:
            read = i2c_msg.read(HM3301_I2C_ADDR_READ >> 1, DATA_CNT)
            self.smbus.i2c_rdwr(read)
            data = list(read)
            print("Raw data received:", data)  # Debugging: Print raw data

        # Check if CRC is valid
            if self.check_crc(data):
                return data
            else:
                print("CRC error!")
                return None
        except Exception as e:
            print(f"I2C Read Error: {e}")
            return None

    def check_crc(self, data):
        # Calculate checksum as sum of bytes 0-28 modulo 256
        checksum = sum(data[:-1]) % 256
        return checksum == data[-1]

    def parse_data(self, data):
        if data:
            # Parse particulate matter concentrations (Standard & Atmospheric)
            pm1_0_std = (data[4] << 8) | data[5]
            pm2_5_std = (data[6] << 8) | data[7]
            pm10_std = (data[8] << 8) | data[9]

            pm1_0_atm = (data[10] << 8) | data[11]
            pm2_5_atm = (data[12] << 8) | data[13]
            pm10_atm = (data[14] << 8) | data[15]

            print(f"PM1.0 (Standard): {pm1_0_std} µg/m³")
            print(f"PM2.5 (Standard): {pm2_5_std} µg/m³")
            print(f"PM10  (Standard): {pm10_std} µg/m³")

            print(f"PM1.0 (Atmospheric): {pm1_0_atm} µg/m³")
            print(f"PM2.5 (Atmospheric): {pm2_5_atm} µg/m³")
            print(f"PM10  (Atmospheric): {pm10_atm} µg/m³")
        else:
            print("No data to parse.")

    def close(self):
        self.smbus.close()

def main():
    sensor = HM3301Sensor()
    print("Allowing sensor to warm up...")
    time.sleep(30)  # Initial warm-up time for sensor stabilization

    try:
        while True:
            data = sensor.read_data()
            if data:
                sensor.parse_data(data)
            time.sleep(5)  # Delay between readings
    except KeyboardInterrupt:
        pass
    finally:
        sensor.close()

if __name__ == '__main__':
    main()
