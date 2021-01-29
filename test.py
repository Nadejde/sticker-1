import time
from DRV8825 import DRV8825
import random
import grabber
import movement
from signal import pause
import camera
import threading
import concurrent.futures

Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
Motor1.SetMicroStep('hardward','fullstep')
Motor2.SetMicroStep('hardward','fullstep')
Motor1.Stop()
Motor2.Stop()


def go_to_grab(future_number):
    steps_down = movement.move_down(Motor2)
    next_number = future_number.result()
    if(next_number != None):
        p1 = threading.Thread(target=grabber.grab, name ="grab")
        p1.start()
    movement.move_up(Motor2, steps_down)
    steps_down = 0
    return next_number

def go_to_release():
    steps_down = movement.move_down(Motor2)
    p1 = threading.Thread(target=grabber.release, name="release")
    p1.start()
    movement.move_up(Motor2, 50)
    movement.move_up(Motor2, steps_down)
    steps_down = 0

def read_next_number():
    next_number = camera.get_sticker_number('Panini - Football 2020')
    print(next_number)
    return next_number

current_position = 1


try:
    time.sleep(2) #camera warmup
    start_time = time.time()

    for x in range(1,10):
        print('at position: ' + str(x))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(read_next_number)
            next_number = go_to_grab(future)
            if(next_number == None): 
                break

            print('got sticker number: ' + next_number)
            next = random.randint(5,8)
            print('go to position: ' + str(next))
            current_position = movement.move_to_position(Motor1, current_position, next)
        
            go_to_release()
            print('released sticker number: ' + next_number)
            current_position = movement.move_to_position(Motor1, current_position, 1)
            executor.shutdown()

        

    #current_position = movement.move_to_position(Motor1, current_position, 10)
    #time.sleep(5)
    current_position = movement.move_to_position(Motor1, current_position, 1)
    Motor1.Stop()

    end_time = time.time()
    print("total time: " + str(end_time - start_time))
    
    Motor2.Stop()
    Motor1.Stop()
    pause()


except Exception as e:
    print(e)

finally:
    camera.stop()
    Motor2.Stop()
    Motor1.Stop()
    pause()

    
