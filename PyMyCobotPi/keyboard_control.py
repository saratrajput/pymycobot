import time

# Variables needed to initialize MyCobot Pi
from pymycobot import PI_BAUD, PI_PORT
from pymycobot.genre import Angle
from pymycobot.mycobot import MyCobot
from functools import partial
import zmq

port = "8000"

# Socket to talk to server
context = zmq.Context()
sub = context.socket(zmq.SUB)
sub.setsockopt(zmq.SUBSCRIBE, b"")
print("Subscriber connecting...")
sub.connect("tcp://192.168.0.108:{}".format(port))
# sub.connect("tcp://192.168.0.113:{}".format(port))


class MyCobotPi():
    def __init__(self):
        # Initialize MyCobot object
        self.mc = MyCobot(PI_PORT, PI_BAUD)
        # If you decrease speed increase sleep time
        self.speed = 30
        self.sleep_time = 2.5
        self.joint_dict = {1: "J1", 2: "J3", 3: "J4", 4: "J5", 5: "J6"}

        self.current_joint = 2

    def set_zero_position(self):
        # Set zero position and speed
        zero_position = [0, 0, 0, 0, 0, 0]

        self.mc.send_angles(zero_position, self.speed)
        print(self.mc.is_paused())
        time.sleep(2.5)

    def move_joint(self):
        print("Moving joint")
        self.mc.jog_angle(self.current_joint, 1, self.speed)

    def stop_movement(self):
        print("Stopping joint")
        self.mc.jog_stop()

    def move_opposite(self):
        print("Moving joint")
        self.mc.jog_angle(self.current_joint, 0, self.speed)

    def set_current_joint(self, joint_num):
        if joint_num != self.current_joint:
            self.current_joint = joint_num
            print("Current Joint: {}".format(self.current_joint - 1))


if __name__ == "__main__":
    mc = MyCobotPi()
    mc.set_zero_position()

    last_command = ""

    while True:
        my_string = sub.recv_string()
        my_int = int(my_string)

        if my_string == last_command:
            continue
        else:
            last_command = my_string
        if my_int > 0 and my_int < 7:
            # Select Joint
            mc.set_current_joint(my_int+1) 
        if my_string == "7":
            # Forward Jog
            mc.move_joint()
        elif my_string == "0":
            mc.stop_movement()
        elif my_string == "8":
            mc.move_opposite()
