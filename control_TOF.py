
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import L298N as HBridge
import VL53L1X
import time
import threading
import sys

# Motoren Funktionen
speedleft = 0
speedright = 0

sensor_lock = threading.Lock()


# Drive forward
def forward(speed_increase):
    print("drive forward")
    global speedleft
    global speedright
    speedleft = speedleft + speed_increase
    speedright = speedright + speed_increase
    if speedleft > 0.6:
        speedleft = 0.6
    if speedright > 0.6:
        speedright = 0.6
    HBridge.Motor.setMotorLeft(speedleft)
    HBridge.Motor.setMotorRight(speedright)

# Drive backward
def backward(speed_increase):
    print("drive backward")
    global speedleft
    global speedright
    speedleft = speedleft - speed_increase
    speedright = speedright - speed_increase
    if speedleft < -1:
        speedleft = -1
    if speedright < -1:
        speedright = -1
    HBridge.Motor.setMotorLeft(speedleft)
    HBridge.Motor.setMotorRight(speedright)

# Stop
def stop():
    print("stop")
    global speedleft
    global speedright
    speedleft = 0
    speedright = 0
    HBridge.Motor.setMotorLeft(speedleft)
    HBridge.Motor.setMotorRight(speedright)


def left(speed_increase):
    print("drive left")
    global speedleft
    global speedright
    speedleft = max(speedleft - speed_increase, 0)  # Stellen Sie sicher, dass speedleft nicht unter 0 fällt
    speedright = min(speedright + speed_increase, 0.6)  # Stellen Sie sicher, dass speedright nicht über 0,5 steigt
    HBridge.Motor.setMotorLeft(speedleft)
    HBridge.Motor.setMotorRight(speedright)



def right(speed_increase):
    print("drive right")
    global speedleft
    global speedright
    speedright = max(speedright - speed_increase, 0)  # Stellen Sie sicher, dass speedright nicht unter 0 fällt
    speedleft = min(speedleft + speed_increase, 0.6)  # Stellen Sie sicher, dass speedleft nicht über 0,5 steigt
    HBridge.Motor.setMotorLeft(speedleft)
    HBridge.Motor.setMotorRight(speedright)



# GPIO Pin-Nummern für die XSHUT-Pins der Sensoren
SENSOR1_XSHUT_PIN = 17
SENSOR2_XSHUT_PIN = 18

# Initialisiere die GPIO-Pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR1_XSHUT_PIN, GPIO.OUT)
GPIO.setup(SENSOR2_XSHUT_PIN, GPIO.OUT)

# Dieser Abschnitt ist für die Initialisierung der Sensoren notwendig, sonst werden die Sensoren nicht erkannt
##############################################################################################################
# Aktiviere Sensor 1
GPIO.output(SENSOR1_XSHUT_PIN, GPIO.HIGH)
# Deaktiviere Sensor 2
GPIO.output(SENSOR2_XSHUT_PIN, GPIO.LOW)
# Initialisiere den Sensor 1
sensor1 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
# Initialisiere den Sensor 2
sensor2 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
##############################################################################################################

# Öffne die Sensoren
sensor1.open()
sensor2.open()


# Sensor Funktionen
# Sensor links
def sensor_right():
    GPIO.output(SENSOR2_XSHUT_PIN, GPIO.LOW)  # Deaktiviere Sensor 2
    GPIO.output(SENSOR1_XSHUT_PIN, GPIO.HIGH) # Aktiviere Sensor 1 und lese ihn einmal aus
    sensor1.start_ranging()
    distance_mm = sensor1.get_distance()
    sensor1.stop_ranging()
    print(f"Sensor rechts - Distance: {distance_mm} mm")
    GPIO.output(SENSOR1_XSHUT_PIN, GPIO.LOW)  # Deaktiviere Sensor 1
    return distance_mm

# Sensor rechts
def sensor_left():
    GPIO.output(SENSOR1_XSHUT_PIN, GPIO.LOW)  # Deaktiviere Sensor 1
    GPIO.output(SENSOR2_XSHUT_PIN, GPIO.HIGH) # Aktiviere Sensor 2 und lese ihn einmal aus
    sensor2.start_ranging()
    distance_mm = sensor2.get_distance()
    sensor2.stop_ranging()
    print(f"Sensor links - Distance: {distance_mm} mm")
    GPIO.output(SENSOR2_XSHUT_PIN, GPIO.LOW)  # Deaktiviere Sensor 2
    return distance_mm

# Funktion um beide Sensoren gleichzeitig auszulesen
def read_sensors():
    while True:
        sensor_right()
        time.sleep(1/25)
        sensor_left()
        time.sleep(1/25)

# Autonomer Modus
def autonomous_mode():
    while True:
        # Lies die Sensordaten
        with sensor_lock:
            right_distance = sensor_right()
            left_distance = sensor_left()

        if right_distance < 700:
            right(speed_increase=0.2)  # Rechts drehen
        elif right_distance > 550 and left_distance > 450:
            forward(speed_increase=0.2)  # Vorwärts fahren

        if left_distance < 700:
            left(speed_increase=0.2)  # Links drehen
        elif left_distance > 550 and right_distance > 450:
            forward(speed_increase=0.2)  # Vorwärts fahren

        #time.sleep(0.1)  # Warte für eine kurze Zeitspanne


# Test um beide Sensoren gleichzeitig auszulesen
def test_sensors():
    for i in range(10):
        sensor_right()
        time.sleep(1/25)
        sys.stdout.flush()
        sensor_left()
        time.sleep(1/25)
        sys.stdout.flush()


def main():
    # Starte den Thread für den autonomen Modus
    autonomous_thread = threading.Thread(target=autonomous_mode)
    autonomous_thread.daemon = True  # Setze den Thread als Hintergrundthread
    autonomous_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        with sensor_lock:
            stop()




if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        with sensor_lock:
            stop()
            GPIO.cleanup()

        GPIO.cleanup(SENSOR2_XSHUT_PIN)
        GPIO.cleanup(SENSOR1_XSHUT_PIN)
