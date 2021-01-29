import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825
import random
from gpiozero import Button

ADUJUSTMENT = 55
SHORT_RUN_ADJUSTMENT = 50
DELAY = 0.0005
SHORT_RUN_DELAY = 0.0007
current_position = 1
GAP = 86.25
MAX_POSITION = 10
THEORETICAL = 3.3333
DOWN_PRECISION = 50
crash = Button(25)

def move_down(motor):
    total_steps = 0
    while(not crash.is_active):
         motor.TurnStep(Dir='backward', steps=DOWN_PRECISION, stepdelay=0.0005)
         #print("test 10 steps")
         total_steps = total_steps + DOWN_PRECISION
    
    motor.Stop()
    return total_steps

def move_up(motor, steps):
    motor.TurnStep(Dir='forward', steps=steps, stepdelay=0.0005)
    motor.Stop()


def move_to_position(motor, start=1, end=1):
    direction = 'backward'
    distance = 0
    stepdelay = DELAY
    adj = ADUJUSTMENT
    if(end > start):
        direction = 'backward'
        distance = (end - start) * GAP
        
    else:
        direction = 'forward'
        distance = (start - end) * GAP
    
    if(distance < 150):
        stepdelay = SHORT_RUN_DELAY
        adj = SHORT_RUN_ADJUSTMENT
    
    steps = int(distance * THEORETICAL) - adj
    if (steps < 0):
        return start
    
    if(end == 1 or end == 9):
        steps = steps + 50

    motor.TurnStep(Dir=direction, steps=steps, stepdelay=stepdelay)
    motor.Stop()

    return end
