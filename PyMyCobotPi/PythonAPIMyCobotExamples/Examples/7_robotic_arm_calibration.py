# -*- coding: UTF-8 -*-
#!/usr/bin/python3
from pymycobot.mycobot import MyCobot
# Variables needed to initialize MyCobotPi
from pymycobot import PI_PORT, PI_BAUD


# Initialize MyCobotPi
mc = MyCobot(PI_PORT, PI_BAUD)

# Check if the controller is connected
if mc.is_controller_connected() != 1:
    print("Please connect the robot arm correctly for writing the program.")
    exit(0)

# Make fine adjustments to the robotic arm to ensure that all the bayonet points
# are aligned in the adjusted position
# Subject to the alignment of the bayonet of the robotic arm, here is just a case
mc.send_angles([0, 0, 18, 0, 0, 0], 20)

# Calibrate the position at this time, the calibrated angular position represents
# [0,0,0,0,0,0], and the potential value represents [2048,2048,2048,2048,2048,2048]
# The for loop is equivalent to the set_gripper_ini() method
for i in range(1, 7):
    mc.set_servo_calibration(i)
