from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


sensor_data = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

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
