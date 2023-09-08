from flask import Flask, request, jsonify
from flask_cors import CORS
import L298N as HBridge
import subprocess
import os
import signal

app = Flask(__name__)
autonomous_process = None
cors = CORS(app, resources={r"/*": {"origins": "http://192.168.4.1:5000"}})
#cors = CORS(app, resources={r"/*": {"origins": "http://10.2.6.102:8888"}})
app = Flask(__name__, static_folder='./web/build', static_url_path='/')

speedleft = 0
speedright = 0
speedfrontleft = 0
speedfrontright = 0
speedbackleft = 0
speedbackright = 0


@app.route('/')
def index():
    return app.send_static_file('index.html')

def set_motor_speeds():
    HBridge.Motorsudo.setMotorLeft(speedleft)
    HBridge.Motor.setMotorRight(speedright)
    HBridge.Motor.set_front_motor_left(speedfrontleft)
    HBridge.Motor.set_front_motor_right(speedfrontright)
    HBridge.Motor.set_rear_motor_left(speedbackleft)
    HBridge.Motor.set_rear_motor_right(speedbackright)

@app.route('/forward', methods=['GET'])
def forward():
    global speedleft, speedright
    speedleft += 0.1
    speedright += 0.1
    if speedleft > 1:
        speedleft = 1
    if speedright > 1:
        speedright = 1
    HBridge.Motor.setMotorLeft(speedleft)
    HBridge.Motor.setMotorRight(speedright)
    return jsonify({'message': 'Forward', 'speed_left': speedleft, 'speed_right': speedright})

@app.route('/backward', methods=['GET'])
def backward():
    global speedleft, speedright
    speedleft -= 0.1
    speedright -= 0.1
    if speedleft < -1:
        speedleft = -1
    if speedright < -1:
        speedright = -1
    HBridge.Motor.setMotorLeft(speedleft)
    HBridge.Motor.setMotorRight(speedright)
    return jsonify({'message': 'Backward', 'speed_left': speedleft, 'speed_right': speedright})

@app.route('/left', methods=['GET'])
def left():
    global speedleft, speedright
    speedleft -= 0.1
    speedright += 0.1
    if speedleft < -1:
        speedleft = -1
    if speedright > 1:
        speedright = 1
    HBridge.Motor.setMotorLeft(speedleft)
    HBridge.Motor.setMotorRight(speedright)
    return jsonify({'message': 'Left', 'speed_left': speedleft, 'speed_right': speedright})

@app.route('/right', methods=['GET'])
def right():
    global speedleft, speedright
    speedleft += 0.1
    speedright -= 0.1
    if speedleft > 1:
        speedleft = 1
    if speedright < -1:
        speedright = -1
    HBridge.Motor.setMotorLeft(speedleft)
    HBridge.Motor.setMotorRight(speedright)
    return jsonify({'message': 'Right', 'speed_left': speedleft, 'speed_right': speedright})

@app.route('/sidestepleft', methods=['GET'])
def sidestepleft():
    global speedfrontleft, speedfrontright, speedbackleft, speedbackright
    speedfrontleft -= 0.1
    speedfrontright += 0.1
    speedbackleft += 0.1
    speedbackright -= 0.1
    if speedfrontleft < -1:
        speedfrontleft = -1
    if speedfrontright > 1:
        speedfrontright = 1
    if speedbackleft > 1:
        speedbackleft = 1
    if speedbackright < -1:
        speedbackright = -1
    HBridge.Motor.set_front_motor_left(speedfrontleft)
    HBridge.Motor.set_front_motor_right(speedfrontright)
    HBridge.Motor.set_rear_motor_left(speedbackleft)
    HBridge.Motor.set_rear_motor_right(speedbackright)
    return jsonify({'message': 'Sidestep Left', 'speed_front_left': speedfrontleft, 'speed_front_right': speedfrontright, 'speed_back_left': speedbackleft, 'speed_back_right': speedbackright})

@app.route('/sidestepright', methods=['GET'])
def sidestepright():
    global speedfrontleft, speedfrontright, speedbackleft, speedbackright
    speedfrontleft += 0.1
    speedfrontright -= 0.1
    speedbackleft -= 0.1
    speedbackright += 0.1
    if speedfrontleft > 1:
        speedfrontleft = 1
    if speedfrontright < -1:
        speedfrontright = -1
    if speedbackleft < -1:
        speedbackleft = -1
    if speedbackright > 1:
        speedbackright = 1
    HBridge.Motor.set_front_motor_left(speedfrontleft)
    HBridge.Motor.set_front_motor_right(speedfrontright)
    HBridge.Motor.set_rear_motor_left(speedbackleft)
    HBridge.Motor.set_rear_motor_right(speedbackright)
    return jsonify({'message': 'Sidestep Right', 'speed_front_left': speedfrontleft, 'speed_front_right': speedfrontright, 'speed_back_left': speedbackleft, 'speed_back_right': speedbackright})




@app.route('/forwardleft', methods=['GET'])
def forwardleft():
    global speedfrontleft, speedfrontright, speedbackleft, speedbackright
    speedfrontleft = 0.0
    speedfrontright += 0.1
    speedbackleft += 0.1
    speedbackright = 0.0
    if speedfrontright > 1:
        speedfrontright = 1
    if speedbackleft > 1:
        speedbackleft = 1
    HBridge.Motor.set_front_motor_left(speedfrontleft)
    HBridge.Motor.set_front_motor_right(speedfrontright)
    HBridge.Motor.set_rear_motor_left(speedbackleft)
    HBridge.Motor.set_rear_motor_right(speedbackright)
    return jsonify({'message': 'Forward Left', 'speed_front_left': speedfrontleft, 'speed_front_right': speedfrontright, 'speed_back_left': speedbackleft, 'speed_back_right': speedbackright})



@app.route('/forwardright', methods=['GET'])
def forwardright():
    global speedfrontleft, speedfrontright, speedbackleft, speedbackright
    speedfrontleft += 0.1
    speedfrontright = 0.0
    speedbackleft = 0.0
    speedbackright += 0.1
    if speedfrontleft > 1:
        speedfrontleft = 1
    if speedbackright > 1:
        speedbackright = 1
    HBridge.Motor.set_front_motor_left(speedfrontleft)
    HBridge.Motor.set_front_motor_right(speedfrontright)
    HBridge.Motor.set_rear_motor_left(speedbackleft)
    HBridge.Motor.set_rear_motor_right(speedbackright)
    return jsonify({'message': 'Forward Right', 'speed_front_left': speedfrontleft, 'speed_front_right': speedfrontright, 'speed_back_left': speedbackleft, 'speed_back_right': speedbackright})


@app.route('/backwardright', methods=['GET'])
def backwardright():
    global speedfrontleft, speedfrontright, speedbackleft, speedbackright
    speedfrontleft = 0.0
    speedfrontright -= 0.1
    speedbackleft -= 0.1
    speedbackright = 0.0
    if speedfrontright < -1:
        speedfrontright = -1
    if speedbackleft < -1:
        speedbackleft = -1
    HBridge.Motor.set_front_motor_left(speedfrontleft)
    HBridge.Motor.set_front_motor_right(speedfrontright)
    HBridge.Motor.set_rear_motor_left(speedbackleft)
    HBridge.Motor.set_rear_motor_right(speedbackright)
    return jsonify({'message': 'Backward Left', 'speed_front_left': speedfrontleft, 'speed_front_right': speedfrontright, 'speed_back_left': speedbackleft, 'speed_back_right': speedbackright})




@app.route('/backwardleft', methods=['GET'])
def backwardleft():
    global speedfrontleft, speedfrontright, speedbackleft, speedbackright
    speedfrontleft -= 0.1
    speedfrontright = 0.0
    speedbackleft = 0.0
    speedbackright -= 0.1
    if speedfrontleft < -1:
        speedfrontleft = -1
    if speedbackright < -1:
        speedbackright = -1
    HBridge.Motor.set_front_motor_left(speedfrontleft)
    HBridge.Motor.set_front_motor_right(speedfrontright)
    HBridge.Motor.set_rear_motor_left(speedbackleft)
    HBridge.Motor.set_rear_motor_right(speedbackright)
    return jsonify({'message': 'Backward Right', 'speed_front_left': speedfrontleft, 'speed_front_right': speedfrontright, 'speed_back_left': speedbackleft, 'speed_back_right': speedbackright})



@app.route('/stop', methods=['GET'])
def stop():
    global speedleft, speedright, speedfrontleft, speedfrontright, speedbackleft, speedbackright
    speedleft = speedright = speedfrontleft = speedfrontright = speedbackleft = speedbackright = 0
    HBridge.Motor.setMotorLeft(speedleft)
    HBridge.Motor.setMotorRight(speedright)
    return jsonify({'message': 'Stop'})

@app.route('/startautonom', methods=['GET'])
def start_autonomous():
    global autonomous_process
    try:
        if autonomous_process is None:
            autonomous_process = subprocess.Popen(['python3', 'control_TOF.py'], preexec_fn=os.setsid, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return jsonify(message="Autonomer Modus gestartet."), 200
        else:
            return jsonify(message="Autonomer Modus läuft bereits."), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/stopautonom', methods=['GET'])
def stop_autonomous():
    global autonomous_process
    try:
        if autonomous_process is not None:
            os.killpg(os.getpgid(autonomous_process.pid), signal.SIGINT)
            stdout, stderr = autonomous_process.communicate()
            print("Autonomous Process STDOUT:", stdout.decode('utf-8'))
            print("Autonomous Process STDERR:", stderr.decode('utf-8'))
            autonomous_process = None
            return jsonify(message="Autonomer Modus gestoppt."), 200
        else:
            return jsonify(message="Autonomer Modus läuft nicht."), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


# Implement other endpoints similarly

if __name__ == '__main__':
    app.run(host='192.168.4.1', port=5000)
    #app.run(host='10.2.6.102', port=8888)
