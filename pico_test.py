import network
import urequests
import time

ssid = 'test123'         # Replace with your Wi-Fi SSID
password = '12345678' # Replace with your Wi-Fi password

server_ip = '10.42.0.163'

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    max_wait = 15
    while max_wait > 0:
        if wlan.isconnected():
            print('Connected to WiFi')
            print('IP:', wlan.ifconfig()[0])
            return wlan
        print('Waiting for connection...')
        time.sleep(1)
        max_wait -= 1
    raise Exception('Failed to connect to WiFi')

def send_data():
    url = f'http://{server_ip}:5000/data'  # Replace with your server's IP
    data = {'sensor_value': 'testing'}  # Replace with your actual data
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = urequests.post(url, json=data, headers=headers)
        print('Response:', response.json())
        response.close()
    except Exception as e:
        print('Failed to send data:', e)

# Main execution
wlan = connect_wifi()
send_data()
