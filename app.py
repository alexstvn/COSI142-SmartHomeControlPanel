from flask import Flask, request, jsonify, render_template, redirect, url_for
from helper.ip import get_local_ip
from helper.kasa_helper import KasaHelper

app = Flask(__name__)

sensor_data = {}
ip = get_local_ip()

automation_rules = []

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
    plug_states = kasa.get_all_plug_states()
    return render_template('devices.html', server_ip=ip, sensor_data=sensor_data, plugs=plug_states, automation_rules=automation_rules)

@app.route('/control')
def control():
    return render_template('control.html')


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
        check_automation_rules(device_id, sensor_data[device_id])
        return jsonify({'status': 'success'}), 200
    
    return jsonify({'status': 'error', 'message': 'Invalid data'}), 400


@app.route('/add_rule', methods=['POST'])
def add_rule():
    device_id = request.form.get('device_id')
    reading = request.form.get('reading')
    operator = request.form.get('operator')
    threshold = request.form.get('threshold', type=float)
    plug_ip = request.form.get('plug_ip')
    action = request.form.get('action')

    if device_id and reading and operator and threshold is not None and action and plug_ip:
        rule = {
            "device_id": device_id,
            "reading": reading,
            "operator": operator,
            "threshold": threshold,
            "plug_ip": plug_ip,
            "action": action
        }
        automation_rules.append(rule)
        return redirect(url_for('devices'))
    else:
        return jsonify({'status': 'error', 'message': 'Invalid rule data'}), 400
    
@app.route('/delete_rule/<int:rule_index>', methods=['POST'])
def delete_rule(rule_index):
    if 0 <= rule_index < len(automation_rules):
        deleted_rule = automation_rules.pop(rule_index)
        return redirect(url_for('devices'))
    else:
        return jsonify({'status': 'error', 'message': 'Invalid rule index'}), 400


def check_automation_rules(device_id, readings):
    plug_states = kasa.get_all_plug_states()  # Update and get current states
    for rule_index, rule in enumerate(automation_rules):
        if rule['device_id'] == device_id:
            sensor_value = readings.get(rule['reading'])
            if sensor_value is not None and evaluate_condition(sensor_value, rule['operator'], rule['threshold']):
                # Condition met - decide what to do with the target plug
                target_plug_ip = rule.get('plug_ip')
                action = rule.get('action')
                
                if target_plug_ip and action in ["on", "off"]:
                    current_state = plug_states.get(target_plug_ip)
                    if current_state:
                        plug_is_on = current_state['is_on']
                        
                        # If action is turn_on and plug is currently off -> turn on
                        if action == "on" and not plug_is_on:
                            print(f"Triggering action for rule {rule_index}: Turning on {target_plug_ip}")
                            kasa.turn_on_plug(target_plug_ip)
                        
                        # If action is turn_off and plug is currently on -> turn off
                        elif action == "off" and plug_is_on:
                            print(f"Triggering action for rule {rule_index}: Turning off {target_plug_ip}")
                            kasa.turn_off_plug(target_plug_ip)
                        # Otherwise, do nothing if the plug is already in the desired state.

def evaluate_condition(sensor_value, operator, threshold):
    if operator == '>':
        return sensor_value > threshold
    elif operator == '<':
        return sensor_value < threshold
    elif operator == '=':
        return sensor_value == threshold
    return False

if __name__ == '__main__':
    # Set host to '0.0.0.0' to make the server accessible externally
    app.run(host='0.0.0.0', port=5000, debug=True)
