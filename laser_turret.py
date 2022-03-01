# controls 2 servos and a laser diode
from gpiozero import LED, Servo
import time
import pickle
from adafruit_servokit import ServoKit

laser = LED(26)
kit = ServoKit(channels=16)
kit.servo[0].actuation_range = 360
kit.servo[1].actuation_range = 360

def go(v, h):
    """ Update the servo locations

    Args:
      v (float): [-180 - 180] value to set the vertical servo to
      h (float): [-180 - 180] value to set the horizontal servo to
    """

    # adjust to new domain, 0-360 vs -180 to 180
    v = v + 180
    h = -h + 180
    if not ((0 <= v <= 360) and (0 <= h <= 360)):
      print(f"{h},{v} out of range -----")
      return;

    kit.servo[0].angle = v
    kit.servo[1].angle = h

def goslow(h, v):

    h_start = kit.servo[1].angle - 180
    v_start = kit.servo[0].angle - 180

    for d in range(1,101):
       h_value = h_start + (h - h_start) * (d/100.0)
       v_value = v_start + (v - v_start) * (d/100.0)
       go(h_value, v_value)
       time.sleep(0.005) 

