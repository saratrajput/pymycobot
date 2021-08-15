# -*- coding: UTF-8 -*-
#!/usr/bin/python3
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
# Variables needed to initialize MyCobot Pi
from pymycobot import PI_PORT, PI_BAUD
import time


# Initialize MyCobot object
mc = MyCobot(PI_PORT, PI_BAUD)

# Get the coordinates of the current location
angle_datas = mc.get_angles()
print(angle_datas)

# Set zero position and speed
zero_position = [0, 0, 0, 0, 0, 0]
# If you decrease speed increase the sleep time
speed = 50

# Use the number sequence to pass the coordinate parameters, so that the robot
# arm can move to the specified position
mc.send_angles(zero_position, speed)
print(mc.is_paused())

# Set the waiting time to ensure that the robotic arm has reached the specified
# position
# while not mc.is_paused():
time.sleep(2.5)

# Move joint1 to the position of 90
mc.send_angle(Angle.J1.value, 90, speed)

# Set the waiting time to ensure that the robotic arm has reached the
# designated position
time.sleep(2)

# Swing the arm left and right
for i in range(2):
    # Move Joint-2 to position of 50
    mc.send_angle(Angle.J2.value, 50, speed)

    # Set the waiting time to ensure that the robotic arm has reached the
    # designated position
    time.sleep(1.5)

    # Move Joint-2 to -50 position
    mc.send_angle(Angle.J2.value, -50, speed)

    # Wait till the joint moves to desired position
    time.sleep(1.5)

# Let the robotic arm retract. You can swing the robotic arm manually, and then
# use the get_angles() function to get the coordinates series
# Use this function to make the robotic arm reach the position you want
mc.send_angles([88.68, -138.51, 155.65, -128.05, -9.93, -15.29], speed)

# Wait till the joint moves to desired position
time.sleep(2.5)

# Release the servos to move the robot manually
mc.release_all_servos()
