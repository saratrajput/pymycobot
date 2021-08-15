# -*- coding: UTF-8 -*-
#!/usr/bin/python3
from pymycobot.mycobot import MyCobot
# Variables needed to initialize MyCobot Pi
from pymycobot import PI_PORT, PI_BAUD
import time


# Initialize MyCobotPi
mc = MyCobot(PI_PORT, PI_BAUD)
# Determine whether the robotic arm is powered, if there is no power supply, it
# needs to be powered first
if not mc.is_power_on():
    # Power the robotic arm
    mc.power_on()
# The robotic arm reaches the position [0, 0, 0, 0, 0, 0] at speed of 30
mc.send_angles([0, 0, 0, 0, 0, 0], 30)
# Get the current time
start = time.time()
# Determine whether the robot arm reaches the position [0, 0, 0, 0, 0, 0]
while not mc.is_in_position([0, 0, 0, 0, 0, 0], 0):
    # Restore the movement of the robotic arm
    mc.resume()
    # Let the robotic arm move 0.5
    time.sleep(0.5)
    # Pause robotic arm movement
    mc.pause()
    # Determine whether the move has timed out
    if time.time() - start > 9:
        # Stop the movement of the robotic arm
        mc.stop()
        break
# Get current time
start = time.time()

desired_position = [88.68, -138.51, 155.65, -128.05, -9.93, -15.29]
speed = 30

# Robotic arm reaches the position at given speed (30)
# mc.send_angles([88.68, -138.51, 155.65, -128.05, -9.93, -15.29], 30)
mc.send_angles(desired_position, speed)

# Check whether the robot arm has reached the position
#while not mc.is_in_position([88.68, -138.51, 155.65, -128.05, -9.93, -15.29], 0):
while not mc.is_in_position(desired_position, 0):
    # Restore the movement of the robotic arm
    mc.resume()
    # Let the robotic arm move for 0.5 s
    time.sleep(0.5)
    # To pause the movement of the robotic arm, you can use is_paused() to
    # determine whether the robotic arm is in a paused state
    mc.pause()
    # Determine whether the move has timed out
    if time.time() - start > 9:
        mc.stop()
        # Stop the movement of the robotic arm
        break
# After performing the operation, power off the robotic arm
mc.power_off()
