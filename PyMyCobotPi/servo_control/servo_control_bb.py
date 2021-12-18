# Import libraries
import RPi.GPIO as GPIO
import time
import zmq

port = "8001"

# Socket to talk to server
context = zmq.Context()
sub = context.socket(zmq.SUB)
sub.setsockopt(zmq.SUBSCRIBE, b"")
print("Subscriber connecting...")
sub.connect("tcp://192.168.0.108:{}".format(port))

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 11 as an output, and set servo1 as pin 11 as PWM
GPIO.setup(11, GPIO.OUT)
servo1 = GPIO.PWM(11, 50) # Note 11 is pin, 50 = 50Hz pulse

# Start PWM running, but with value of 0 (pulse off)
servo1.start(0)

# Loop to allow user to set servo angle. Try/finally allows exit with execution of
# servo.stop and GPIO cleanup

def move_servo_to_angle(angle):
    servo1.ChangeDutyCycle(2+(angle/18))
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)

def most_frequent(List):
    return max(set(List), key = List.count)

open_angle = float(32)
close = float(38)
last_command = ""
last_command_list = []

try:
    while True:

        my_string = sub.recv_string()
        my_int = int(my_string)

        if my_int == last_command:
            continue
        else:
            # for i in range(10):
            #     last_command_list.append(my_string)
            
            last_command = my_int
            # last_command = most_frequent(last_command_list)
        if my_int == 1:
            move_servo_to_angle(open_angle)
            print("Gripper Open")
            # time.sleep(3)
        if my_int == 2:
            move_servo_to_angle(close)
            print("Gripper Close")
            # time.sleep(10)

finally:
    # Clean things up at the end
    servo1.stop()
    GPIO.cleanup()
    print("Goodbye!")
