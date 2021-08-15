# -*- coding: UTF-8 -*-
#!/usr/bin/python3
from pymycobot.mycobot import MyCobot
# Variables needed to initialize MyCobotPi
from pymycobot import PI_PORT, PI_BAUD
import time


# Initialize MyCobotPi
mc = MyCobot(PI_PORT, PI_BAUD)
# Turn on the robot if it's not already powered on
if not mc.is_power_on():
    # Turn on the robot
    mc.power_on()

# Check whether the six joints are working properly
# You can also use is_servo_enable(servo_id) to change a single check
if mc.is_all_servo_enable():
    # Power off the robotic arm
    mc.power_off()
    # Determine whether the robotic arm is powered off
    if mc.is_all_servo_enable() == -1:
        print("The power supply of the robotic arm is normal.")
    else:
        print("Power failure of the robotic arm.")
        exit(0)

# Power on the robotic arm
mc.power_on()

# Set the robotic arm to zero position
zero_position = [0, 0, 0, 0, 0, 0]
speed = 30
# mc.send_angles([0, 0, 0, 0, 0, 0], 30)
mc.send_angles(zero_position, speed)

# Get the current time
start = time.time()
# Determine if the robot reaches the desired position
# while not mc.is_in_position([0, 0, 0, 0, 0, 0], 0):
while not mc.is_in_position(zero_position, 0):
    # Resume robotic arm movement
    mc.resume()
    # Let the arm move for 0.5s
    time.sleep(0.5)
    # Pause robotic arm's movement
    mc.pause()
    # Determine whether the move has timed out
    if time.time() - start > 9:
        # Stop moving the robotic arm
        print("Arm failed to move to zero position.")
        # Abort procedure
        exit(0)

# Detect the movement of the six joints
for i in range(1, 7):
    # Move the joint point i to the right at a speed of 15
    mc.jog_angle(i, 0, 15)
    # Move the joint point 1.5s
    time.sleep(1.5)
    # Stop joint point movement
    mc.jog_stop()
    # Move the joint point i to the left at a speed of 15
    mc.jog_angle(i, 1, 15)
    # Move the joint point for 3s
    time.sleep(3)
    # Stop joint point movement
    mc.jog_stop()
    # Move the joint point i to the right at a speed of 15
    mc.jog_angle(i, 0, 15)
    # Move the joint point for 1.5s
    time.sleep(1.5)
    # Stop joint point movement
    mc.jog_stop()
    print(str(i) + "No. Joint Point works normally.")
    # Wait 0.8s
    time.sleep(0.8)

# Get the current time
start = time.time()
# Set desired position and speed
desired_position = [87.27, -139.13, 153.72, -160.92, -74.44, 7.55]
speed = 30
# Move the arm to desired position at given speed
mc.send_angles(desired_position, speed)

# Wait till the arm reaches the desired position and stops
# while not mc.is_in_position([87.27, -139.13, 153.72, -160.92, -74.44, 7.55], 0):
while not mc.is_in_position(desired_position, 0):
    # Resume the robotic arm's movement
    mc.resume()
    # Let the robotic arm move for 0.5s
    time.sleep(0.5)
    # Pause robotic arm movement
    mc.pause()
    # Determine whether the move has timed out
    if time.time() - start > 9:
        mc.stop()
        # Stop the robotic arm's movement
        break

# Release all servos
for i in range(1, 7):
    mc.release_servo(i)
