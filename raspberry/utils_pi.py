import requests
import time

def send_data(server_ip, data):
    """
    Sends data to the specified server IP using the HTTP POST method.

    Args:
        server_ip (str): The server's IP address.
        data (dict): The data to be sent.
    """
    url = f'http://{server_ip}:5000/data'
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=data, headers=headers)
        print('Response:', response.json())
    except Exception as e:
        print('Failed to send data:', e)
