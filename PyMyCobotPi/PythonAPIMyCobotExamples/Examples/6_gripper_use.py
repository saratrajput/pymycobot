# -*- coding: UTF-8 -*-
#!/usr/bin/python3
# Variables needed to initialize MyCobot Pi
from pymycobot import PI_PORT, PI_BAUD
from pymycobot.mycobot import MyCobot
import time


def gripper_test(mc):
    print("Start check IO part of api\n")
    # Check if the gripper is moving
    flag = mc.is_gripper_moving()
    print("Is gripper moving: {}".format(flag))
    time.sleep(1)

    # Set the current position to (2048).
    # Use it when you are sure you need it.
    # Gripper has been initialized for a long time. Generally, there
    # is no need to change the method.
    # mc.set_gripper_ini()
    # Set joint point 1 and let it rotate to the position of 2048
    mc.set_encoder(1, 2048)
    time.sleep(2)
    # Set up six joint positions and let the robotic arm rotate to this position
    # at a speed of 20
    mc.set_encoders([1024, 1024, 1024, 1024, 1024, 1024], 20)
    time.sleep(3)
    # Get the position information of Joint-1
    print(mc.get_encoder(1))
    # Set the gripper to rotate to 2048 position
    mc.set_encoder(7, 2048)
    time.sleep(3)
    # Set the gripper to turn it to the 1300 position
    mc.set_encoder(7, 1300)
    time.sleep(3)

    # Let the gripper reach the 2048 state at a speed of 70
    mc.set_gripper_value(2048, 70)
    time.sleep(3)
    # Let the gripper reach the 1500 state at a speed of 70
    mc.set_gripper_value(1500, 70)
    time.sleep(3)

    # Set the state of the gripper and let it quickly open the gripper at a speed
    # of 70
    mc.set_gripper_state(0, 70)
    time.sleep(3)
    # Set the state of the gripper to quickly close the gripper at a speed of 70
    mc.set_gripper_state(1, 70)
    time.sleep(3)

    # Get the value of the gripper
    print("")
    print(mc.get_gripper_value())


if __name__ == "__main__":
    # Initialize MyCobotPi
    mc = MyCobot(PI_PORT, PI_BAUD)
    # Move it to the zero position
    mc.set_encoders([2048, 2048, 2048, 2048, 2048, 2048], 20)
    time.sleep(3)
    gripper_test(mc)
