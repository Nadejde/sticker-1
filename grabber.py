from gpiozero import Button
from signal import pause
import board
import digitalio
import busio
import time
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

SUCTION_STEPS = 200

#button = Button(25)
kit = MotorKit(i2c=board.I2C())

def grab():
    for i in range(SUCTION_STEPS):
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        #time.sleep(0.0005)
    kit.stepper1.release()

def release():
    for i in range(SUCTION_STEPS+100):
        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        #time.sleep(0.0005)
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        #time.sleep(0.0005)
    kit.stepper1.release()







 
