from __future__ import division
import RPi.GPIO as io
from PCA9685 import PCA9685


io.setmode(io.BCM)
PCA9685_pwm = PCA9685(address=0x40)
PCA9685_pwm.set_pwm_freq(60)
duty_cycle = 4095
DC_MAX = 100
io.setwarnings(False)

front_left_motor_in1_pin = 6
front_left_motor_in2_pin = 13
front_right_motor_in1_pin = 19
front_right_motor_in2_pin = 26

io.setup(front_left_motor_in1_pin, io.OUT)
io.setup(front_left_motor_in2_pin, io.OUT)
io.setup(front_right_motor_in1_pin, io.OUT)
io.setup(front_right_motor_in2_pin, io.OUT)

io.output(front_left_motor_in1_pin, False)
io.output(front_left_motor_in2_pin, False)
io.output(front_right_motor_in1_pin, False)
io.output(front_right_motor_in2_pin, False)

# ...

rear_left_motor_in1_pin = 12
rear_left_motor_in2_pin = 16
rear_right_motor_in1_pin = 20
rear_right_motor_in2_pin = 21

io.setup(rear_left_motor_in1_pin, io.OUT)
io.setup(rear_left_motor_in2_pin, io.OUT)
io.setup(rear_right_motor_in1_pin, io.OUT)
io.setup(rear_right_motor_in2_pin, io.OUT)

io.output(rear_left_motor_in1_pin, False)
io.output(rear_left_motor_in2_pin, False)
io.output(rear_right_motor_in1_pin, False)
io.output(rear_right_motor_in2_pin, False)

# ...

def setFrontMotorMode(motor, mode):
    if motor == "leftmotor":
        if mode == "reverse":
            io.output(front_left_motor_in1_pin, True)
            io.output(front_left_motor_in2_pin, False)
        elif mode == "forward":
            io.output(front_left_motor_in1_pin, False)
            io.output(front_left_motor_in2_pin, True)
        else:
            io.output(front_left_motor_in1_pin, False)
            io.output(front_left_motor_in2_pin, False)
    elif motor == "rightmotor":
        if mode == "reverse":
            io.output(front_right_motor_in1_pin, False)
            io.output(front_right_motor_in2_pin, True)
        elif mode == "forward":
            io.output(front_right_motor_in1_pin, True)
            io.output(front_right_motor_in2_pin, False)
        else:
            io.output(front_right_motor_in1_pin, False)
            io.output(front_right_motor_in2_pin, False)
    else:
        io.output(front_left_motor_in1_pin, False)
        io.output(front_left_motor_in2_pin, False)
        io.output(front_right_motor_in1_pin, False)
        io.output(front_right_motor_in2_pin, False)

# ...



def setRearMotorMode(motor, mode):
    if motor == "leftmotor":
        if mode == "reverse":
            io.output(rear_left_motor_in1_pin, True)
            io.output(rear_left_motor_in2_pin, False)
        elif mode == "forward":
            io.output(rear_left_motor_in1_pin, False)
            io.output(rear_left_motor_in2_pin, True)
        else:
            io.output(rear_left_motor_in1_pin, False)
            io.output(rear_left_motor_in2_pin, False)
    elif motor == "rightmotor":
        if mode == "reverse":
            io.output(rear_right_motor_in1_pin, False)
            io.output(rear_right_motor_in2_pin, True)
        elif mode == "forward":
            io.output(rear_right_motor_in1_pin, True)
            io.output(rear_right_motor_in2_pin, False)
        else:
            io.output(rear_right_motor_in1_pin, False)
            io.output(rear_right_motor_in2_pin, False)
    else:
        io.output(rear_left_motor_in1_pin, False)
        io.output(rear_left_motor_in2_pin, False)
        io.output(rear_right_motor_in1_pin, False)
        io.output(rear_right_motor_in2_pin, False)

# ...
class Motor:
    def __init__(self, name, mode, power):
        self.name = name
        self.mode = mode
        self.power = power

    # Beide Seiten Links
    @staticmethod
    def setMotorLeft(power):
        if power < 0:
            setFrontMotorMode("leftmotor", "reverse")
            setRearMotorMode("leftmotor", "reverse")
            pwm = -int(duty_cycle * power)
            if pwm < -duty_cycle:
                pwm = -duty_cycle
        elif power > 0:
            setFrontMotorMode("leftmotor", "forward")
            setRearMotorMode("leftmotor", "forward")
            pwm = int(duty_cycle * power )
            if pwm > duty_cycle:
                pwm = duty_cycle
        else:
            setFrontMotorMode("leftmotor", "stopp")
            setRearMotorMode("leftmotor", "stopp")
            pwm = 0
        PCA9685_pwm.set_pwm(0, 0, pwm)
        PCA9685_pwm.set_pwm(2, 0, pwm)


    # Beide Seiten Rechts
    @staticmethod
    def setMotorRight(power):
        if power < 0:
            setFrontMotorMode("rightmotor", "reverse")
            setRearMotorMode("rightmotor", "reverse")
            pwm = -int(duty_cycle * power)
            if pwm < -duty_cycle:
                pwm = -duty_cycle
        elif power > 0:
            setFrontMotorMode("rightmotor", "forward")
            setRearMotorMode("rightmotor", "forward")
            pwm = int(duty_cycle * power )
            if pwm > duty_cycle:
                pwm = duty_cycle
        else:
            setFrontMotorMode("rightmotor", "stopp")
            setRearMotorMode("rightmotor", "stopp")
            pwm = 0
        PCA9685_pwm.set_pwm(1, 0, pwm)
        PCA9685_pwm.set_pwm(3, 0, pwm)

    # Linker Motor vorne
    @staticmethod
    def set_front_motor_left(power):
        if power < 0:
            setFrontMotorMode("leftmotor", "reverse")
            pwm = -int(duty_cycle * power)
            if pwm < -duty_cycle:
                pwm = -duty_cycle
        elif power > 0:
            setFrontMotorMode("leftmotor", "forward")
            pwm = int(duty_cycle * power)
            if pwm > duty_cycle:
                pwm = duty_cycle
        else:
            setFrontMotorMode("leftmotor", "stopp")
            pwm = 0
        PCA9685_pwm.set_pwm(0, 0, pwm)

    # Rechter Motor hinten
    @staticmethod
    def set_rear_motor_left(power):
        if power < 0:
            setRearMotorMode("leftmotor", "reverse")
            pwm = -int(duty_cycle * power)
            if pwm < -duty_cycle:
                pwm = -duty_cycle
        elif power > 0:
            setRearMotorMode("leftmotor", "forward")
            pwm = int(duty_cycle * power)
            if pwm > duty_cycle:
                pwm = duty_cycle
        else:
            setRearMotorMode("leftmotor", "stopp")
            pwm = 0
        PCA9685_pwm.set_pwm(2, 0, pwm)

    # Rechter Motor vorne
    @staticmethod
    def set_front_motor_right(power):
        if power < 0:
            setFrontMotorMode("rightmotor", "reverse")
            pwm = -int(duty_cycle * power)
            if pwm < -duty_cycle:
                pwm = -duty_cycle
        elif power > 0:
            setFrontMotorMode("rightmotor", "forward")
            pwm = int(duty_cycle * power)
            if pwm > duty_cycle:
                pwm = duty_cycle
        else:
            setFrontMotorMode("rightmotor", "stopp")
            pwm = 0
        PCA9685_pwm.set_pwm(1, 0, pwm)

    # Linker Motor hinten
    @staticmethod
    def set_rear_motor_right(power):
        if power < 0:
            setRearMotorMode("rightmotor", "reverse")
            pwm = -int(duty_cycle * power)
            if pwm < -duty_cycle:
                pwm = -duty_cycle
        elif power > 0:
            setRearMotorMode("rightmotor", "forward")
            pwm = int(duty_cycle * power)
            if pwm > duty_cycle:
                pwm = duty_cycle
        else:
            setRearMotorMode("rightmotor", "stopp")
            pwm = 0
        PCA9685_pwm.set_pwm(3, 0, pwm)

    # Alle Motoren stoppen
    @staticmethod
    def stop():
        setFrontMotorMode("leftmotor", "stopp")
        setFrontMotorMode("rightmotor", "stopp")
        setRearMotorMode("leftmotor", "stopp")
        setRearMotorMode("rightmotor", "stopp")
        pwm = 0
        PCA9685_pwm.set_pwm(0, 0, pwm)
        PCA9685_pwm.set_pwm(1, 0, pwm)
        PCA9685_pwm.set_pwm(2, 0, pwm)
        PCA9685_pwm.set_pwm(3, 0, pwm)

    # Alle Motoren vorwärts
    @staticmethod
    def forward(power):
        setFrontMotorMode("leftmotor", "forward")
        setFrontMotorMode("rightmotor", "forward")
        setRearMotorMode("leftmotor", "forward")
        setRearMotorMode("rightmotor", "forward")
        pwm = int(duty_cycle * power)
        if pwm > duty_cycle:
            pwm = duty_cycle
        PCA9685_pwm.set_pwm(0, 0, pwm)
        PCA9685_pwm.set_pwm(1, 0, pwm)
        PCA9685_pwm.set_pwm(2, 0, pwm)
        PCA9685_pwm.set_pwm(3, 0, pwm)

    # Alle Motoren rückwärts
    @staticmethod
    def backward(power):
        setFrontMotorMode("leftmotor", "reverse")
        setFrontMotorMode("rightmotor", "reverse")
        setRearMotorMode("leftmotor", "reverse")
        setRearMotorMode("rightmotor", "reverse")
        pwm = int(duty_cycle * power)
        if pwm > duty_cycle:
            pwm = duty_cycle
        PCA9685_pwm.set_pwm(0, 0, pwm)
        PCA9685_pwm.set_pwm(1, 0, pwm)
        PCA9685_pwm.set_pwm(2, 0, pwm)
        PCA9685_pwm.set_pwm(3, 0, pwm)


    # Seitlich rechts. Vorne links vorwärts, vorne rechts rückwärts, hinten links rückwärts, hinten rechts vorwärts
    @staticmethod
    def sideways_right(power):
        setFrontMotorMode("leftmotor", "forward")
        setFrontMotorMode("rightmotor", "reverse")
        setRearMotorMode("leftmotor", "reverse")
        setRearMotorMode("rightmotor", "forward")
        pwm = int(duty_cycle * power)
        if pwm > duty_cycle:
            pwm = duty_cycle
        PCA9685_pwm.set_pwm(0, 0, pwm)  # Vorderer linker Motor
        PCA9685_pwm.set_pwm(1, 0, pwm)  # Vorderer rechter Motor
        PCA9685_pwm.set_pwm(2, 0, pwm)  # Hinterer linker Motor
        PCA9685_pwm.set_pwm(3, 0, pwm)  # Hinterer rechter Motor


    #   Alles ausschalten
    @staticmethod
    def exit():
        io.output(front_left_motor_in1_pin, False)
        io.output(front_left_motor_in2_pin, False)
        io.output(front_right_motor_in1_pin, False)
        io.output(front_right_motor_in2_pin, False)
        io.cleanup()

# def setFrontMotorLeft(power):
#     if power < 0:
#         setFrontMotorMode("leftmotor", "reverse")
#         pwm = -int(duty_cycle * power)
#         if pwm < -duty_cycle:
#             pwm = -duty_cycle
#     elif power > 0:
#         setFrontMotorMode("leftmotor", "forward")
#         pwm = int(duty_cycle * power )
#         if pwm > duty_cycle:
#             pwm = duty_cycle
#     else:
#         setFrontMotorMode("leftmotor", "stopp")
#         pwm = 0
#     PCA9685_pwm.set_pwm(0, 0, pwm)

# ...


# def setMotorLeft(power):
#     if power < 0:
#         setFrontMotorMode("leftmotor", "reverse")
#         setRearMotorMode("leftmotor", "reverse")
#         pwm = -int(duty_cycle * power)
#         if pwm < -duty_cycle:
#             pwm = -duty_cycle
#     elif power > 0:
#         setFrontMotorMode("leftmotor", "forward")
#         setRearMotorMode("leftmotor", "forward")
#         pwm = int(duty_cycle * power )
#         if pwm > duty_cycle:
#             pwm = duty_cycle
#     else:
#         setFrontMotorMode("leftmotor", "stopp")
#         setRearMotorMode("leftmotor", "stopp")
#         pwm = 0
#     PCA9685_pwm.set_pwm(0, 0, pwm)
#     PCA9685_pwm.set_pwm(2, 0, pwm)

# def setFrontMotorRight(power):
#     if power < 0:
#         setFrontMotorMode("rightmotor", "reverse")
#         pwm = -int(duty_cycle * power)
#         if pwm < -duty_cycle:
#             pwm = -duty_cycle
#     elif power > 0:
#         setFrontMotorMode("rightmotor", "forward")
#         pwm = int(duty_cycle * power )
#         if pwm > duty_cycle:
#             pwm = duty_cycle
#     else:
#         setFrontMotorMode("rightmotor", "stopp")
#         pwm = 0
#     PCA9685_pwm.set_pwm(1, 0, pwm)

# # ...

# def setRearMotorLeft(power):
#     if power < 0:
#         setRearMotorMode("leftmotor", "reverse")
#         pwm = -int(duty_cycle * power)
#         if pwm < -duty_cycle:
#             pwm = -duty_cycle
#     elif power > 0:
#         setRearMotorMode("leftmotor", "forward")
#         pwm = int(duty_cycle * power )
#         if pwm > duty_cycle:
#             pwm = duty_cycle
#     else:
#         setRearMotorMode("leftmotor", "stopp")
#         pwm = 0
#     PCA9685_pwm.set_pwm(2, 0, pwm)

# # ...

# def setRearMotorRight(power):
#     if power < 0:
#         setRearMotorMode("rightmotor", "reverse")
#         pwm = -int(duty_cycle * power)
#         if pwm < -duty_cycle:
#             pwm = -duty_cycle
#     elif power > 0:
#         setRearMotorMode("rightmotor", "forward")
#         pwm = int(duty_cycle * power )
#         if pwm > duty_cycle:
#             pwm = duty_cycle
#     else:
#         setRearMotorMode("rightmotor", "stopp")
#         pwm = 0
#     PCA9685_pwm.set_pwm(3, 0, pwm)

# ...





# Tests:

# def testFrontLeftMotor():
    # setFrontMotorLeft(0.25)
    # time.sleep(2)
    # setFrontMotorLeft(1)
    # time.sleep(2)
    # setFrontMotorLeft(0.0)
    # time.sleep(2)
    # setFrontMotorLeft(-0.25)
    # time.sleep(2)
    # setFrontMotorLeft(-1.0)
    # time.sleep(2)
    # setFrontMotorLeft(0.0)

# # ...

# def test_motors():
#     setFrontMotorLeft(1)
#     setFrontMotorRight(1)
#     setRearMotorLeft(1)
#     setRearMotorRight(1)
#     time.sleep(2)
#     setFrontMotorLeft(0)
#     setFrontMotorRight(0)
#     setRearMotorLeft(0)
#     setRearMotorRight(0)
#     setFrontMotorLeft(-1)
#     setFrontMotorRight(-1)
#     setRearMotorLeft(-1)
#     setRearMotorRight(-1)
#     time.sleep(2)
#     setFrontMotorLeft(0)
#     setFrontMotorRight(0)
#     setRearMotorLeft(0)
#     setRearMotorRight(0)
#     setFrontMotorLeft(0.25)
#     setFrontMotorRight(0.25)
#     setRearMotorLeft(0.25)
#     setRearMotorRight(0.25)
#     time.sleep(2)
#     setFrontMotorLeft(0)
#     setFrontMotorRight(0)
#     setRearMotorLeft(0)
#     setRearMotorRight(0)


# # # Main:

# if __name__ == "__main__":
#     try:
#         test_motors()
#         # ... (call other test functions)
#     except KeyboardInterrupt:
#         exit()
