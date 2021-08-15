# -*- coding: UTF-8 -*-
#!/usr/bin/python3
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Coord
# Variables needed to initialize MyCobot Pi
from pymycobot import PI_PORT, PI_BAUD
import time

# Initialize MyCobot object
mc = MyCobot(PI_PORT, PI_BAUD)
# Get the current head angle and posture
coords = mc.get_coords()
print(coords)
# Intelligently plan the route, let the head reach the coordinates of
# [59.9, -65.8, 250.7] in a linear manner, and maintain the posture of [-50.99, 83.14, -52.42]
mc.send_coords([59.9, -65.8, 250.7, -50.99, 83.14, -52.42], 80, 1)
# Set waiting time
time.sleep(1.5)
# 智能规划路线，让头部以线性的方式到达[59.9,-65.8,350.7]这个坐标，以及保持[-50.99,83.14,-52.42]这个姿态
# Intelligently plan the route, let the head reach the coordinates of
# [59.9, -65.8, 350.7] in a linear manner, and maintain the posture of [-50.99, 83.14, -52.42]
mc.send_coords([59.9, -65.8, 350.7, -50.99, 83.14, -52.42], 80, 1)
# Set waiting time
time.sleep(1.5)
# Only change the x-coordinate of the head and set the x-coordinate of the head
# to -40. Let it intelligently plan the route to move the head to the changed
# position
mc.send_coord(Coord.X.value, -40, 70)
