from pymycobot.mycobot import MyCobot
from pymycobot import PI_PORT, PI_BAUD

mc = MyCobot(PI_PORT, PI_BAUD)
mc.set_color(0, 255, 0)
