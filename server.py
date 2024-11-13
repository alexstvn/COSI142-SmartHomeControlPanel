from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    print(f"Received data: {data}")
    return jsonify({'message': 'Data received'}), 200

if __name__ == '__main__':
    # Set host to '0.0.0.0' to make the server accessible externally
    app.run(host='0.0.0.0', port=5000)
