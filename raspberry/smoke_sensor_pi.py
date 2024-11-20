from smbus2 import SMBus, i2c_msg
import time
from utils import send_data

# Constants
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
            init_command = [0x88]
            write = i2c_msg.write(HM3301_I2C_ADDR_WRITE >> 1, init_command)
            self.smbus.i2c_rdwr(write)
            print("Initialization command sent successfully.")
        except Exception as e:
            print(f"Initialization failed: {e}")
        time.sleep(0.5)

    def read_data(self):
        try:
            read = i2c_msg.read(HM3301_I2C_ADDR_READ >> 1, DATA_CNT)
            self.smbus.i2c_rdwr(read)
            data = list(read)
            print("Raw data received:", data)
            if self.check_crc(data):
                return data
            else:
                print("CRC error!")
                return None
        except Exception as e:
            print(f"I2C Read Error: {e}")
            return None

    def check_crc(self, data):
        checksum = sum(data[:-1]) % 256
        return checksum == data[-1]

    def parse_data(self, data):
        if data:
            pm1_0_std = (data[4] << 8) | data[5]
            pm2_5_std = (data[6] << 8) | data[7]
            pm10_std = (data[8] << 8) | data[9]

            pm1_0_atm = (data[10] << 8) | data[11]
            pm2_5_atm = (data[12] << 8) | data[13]
            pm10_atm = (data[14] << 8) | data[15]

            parsed_data = {
                "pm1_0_std": pm1_0_std,
                "pm2_5_std": pm2_5_std,
                "pm10_std": pm10_std,
                "pm1_0_atm": pm1_0_atm,
                "pm2_5_atm": pm2_5_atm,
                "pm10_atm": pm10_atm,
            }
            return parsed_data
        else:
            print("No data to parse.")
            return None

    def close(self):
        self.smbus.close()

def main():
    sensor = HM3301Sensor()
    server_ip = "10.42.0.163"  # Replace with your server's IP

    print("Allowing sensor to warm up...")
    time.sleep(30)

    try:
        while True:
            data = sensor.read_data()
            if data:
                parsed_data = sensor.parse_data(data)
                if parsed_data:
                    payload = {
                        "device_id": "hm3301_sensor",
                        "readings": parsed_data
                    }
                    send_data(server_ip, payload)
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping the sensor script.")
    finally:
        sensor.close()

if __name__ == "__main__":
    main()
