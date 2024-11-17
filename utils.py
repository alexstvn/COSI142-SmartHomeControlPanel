import network
import urequests
import time

def connect_wifi(ssid, password):
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

def send_data(server_ip, data):
    url = f'http://{server_ip}:5000/data'
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = urequests.post(url, json=data, headers=headers)
        print('Response:', response.json())
        response.close()
    except Exception as e:
        print('Failed to send data:', e)