# -*- coding: UTF-8 -*-
#!/usr/bin/python3
from pymycobot.mycobot import MyCobot
# Variables needed to initialize MyCobot Pi
from pymycobot import PI_PORT, PI_BAUD
import time

# Initialize MyCobotPi
mc = MyCobot(PI_PORT, PI_BAUD)

# Turn on the suction pump
def pump_on():
    # Let the position 2 work
    mc.set_basic_output(2, 0)
    # Let the number 5 work
    mc.set_basic_output(5, 0)

# Stop suction pump
def pump_off():
    # Stop position 2
    mc.set_basic_output(2, 1)
    # Stop position 5
    mc.set_basic_output(5, 1)


pump_off()
time.sleep(3)
pump_on()
time.sleep(3)
pump_off()
time.sleep(3)
