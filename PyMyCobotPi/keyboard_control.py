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
sub.connect("tcp://192.168.0.113:{}".format(port))


class MyCobotPi():
    def __init__(self):
        # Initialize MyCobot object
        self.mc = MyCobot(PI_PORT, PI_BAUD)
        # If you decrease speed increase sleep time
        self.speed = 50
        self.sleep_time = 2.5
        self.joint_dict = {1: "J1", 2: "J3", 3: "J4", 4: "J5", 5: "J6"}

        self.current_joint = "J1"

    def set_zero_position(self):
        # Set zero position and speed
        zero_position = [0, 0, 0, 0, 0, 0]

        self.mc.send_angles(zero_position, self.speed)
        print(self.mc.is_paused())
        time.sleep(2.5)

    # def select_joint(self):
    #     pass
    def select_joint(self):
        pass

    def move_joint(self):
        current_j1_angle = self.mc.get_angles()[0]
        self.mc.send_angle(Angle.J1.value, current_j1_angle + 5, self.speed)

    def move_joint_forward(self):
        pass

    def move_joint_backward(self):
        pass


def on_press(key):
    try:
        print('{0} Pressed'.format(
            key.char))
    except AttributeError:
        print('Error. Special Key pressed: {0}'.format(
            key))

def on_release(key):
    print('{0} Released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


if __name__ == "__main__":
    mc = MyCobotPi()

    while True:
        print("Receiving")
        my_string = sub.recv_string()
        if my_string == "w":
            mc.move_joint()
