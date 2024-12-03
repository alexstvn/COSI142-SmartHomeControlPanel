from flask import Flask, request, jsonify, render_template, redirect, url_for
from helper.ip import get_local_ip
from helper.kasa_helper import KasaHelper

app = Flask(__name__)

sensor_data = {}
ip = get_local_ip()

# for smart plug
kasa = KasaHelper()
kasa.discover_plugs()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/devices')
def devices():
    sensor_list = list(sensor_data.keys())
    plug_states = kasa.get_all_plug_states()

    return render_template('devices.html', server_ip=ip, sensor_list=sensor_list, plugs=plug_states)

<<<<<<< HEAD
@app.route('/control')
def control():
    return render_template('control.html')




=======
>>>>>>> c86124aabe758d085f76e7964677b658b4ea2941
@app.route('/on/<path:ip>')
def turn_on(ip):
    kasa.turn_on_plug(ip)
    return redirect(url_for('devices'))

@app.route('/off/<path:ip>')
def turn_off(ip):
    kasa.turn_off_plug(ip)
    return redirect(url_for('devices'))

@app.route('/rename/<path:ip>', methods=['POST'])
def rename(ip):
    new_alias = request.form.get('new_alias')
    if new_alias:
        kasa.rename_plug(ip, new_alias)
    return redirect(url_for('devices'))

@app.route('/data', methods=['GET'])
def get_sensor_data():
    return jsonify(sensor_data)


@app.route('/data', methods=['POST'])
def receive_data():

    # Endpoint for Pico W devices to report sensor data.
    # Example Payload:
    # {
    #     "device_id": "sensor_1",
    #     "readings": {
    #         "temperature": 20,
    #         "humidity": 10
    #     }
    # }

    data = request.json
    device_id = data.get('device_id')
    readings = data.get('readings')  # This should be a dictionary of readings
    
    if device_id and isinstance(readings, dict):
        # Update the datastore with readings for this device
        if device_id not in sensor_data:
            sensor_data[device_id] = {}
        sensor_data[device_id].update(readings)
        
        print(device_id, sensor_data[device_id])
        return jsonify({'status': 'success'}), 200
    
    return jsonify({'status': 'error', 'message': 'Invalid data'}), 400



if __name__ == '__main__':
    # Set host to '0.0.0.0' to make the server accessible externally
    app.run(host='0.0.0.0', port=5000, debug=True)