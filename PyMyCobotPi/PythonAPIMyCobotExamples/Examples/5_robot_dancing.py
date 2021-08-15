# -*- coding: UTF-8 -*-
from pymycobot.mycobot import MyCobot
# Variables needed to initialize MyCobotPi
from pymycobot import PI_PORT, PI_BAUD
import time


if __name__ == '__main__':
    # Initialize MyCobotPi
    mc = MyCobot(PI_PORT, PI_BAUD)
    # Set start time
    start = time.time()

    # Set desired position
    pos_1 = [-1.49, 115, -153.45, 30, -33.42, 137.9]
    speed = 80
    # Move to desired position
    mc.send_angles(pos_1, speed)

    # Wait till arm reaches the desired position
    while not mc.is_in_position(pos_1, 0):
        # Resume robot's movement
        mc.resume()
        # Let the arm move for 0.5s
        time.sleep(0.5)
        # Pause robot's movement
        mc.pause()
        # Break loop after 3s
        if time.time() - start > 3:
            break

    # Set start time
    start = time.time()
    dance_duration = 30
    # Robot dance for set time
    pos_2 = [-1.49, 55, -153.45, 80, 33.42, 137.9]

    while time.time() - start < dance_duration:
        # Move to desired position
        mc.send_angles(pos_1, speed)
        # Change light color
        mc.set_color(0, 0, 50)
        time.sleep(0.7)
        # Move to desired position
        mc.send_angles(pos_2, speed)
        # Change light color
        mc.set_color(0, 50, 0)
        time.sleep(0.7)

    # Release all servos
    mc.release_all_servos()
