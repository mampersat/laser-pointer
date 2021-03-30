# controls 2 servos and a laser diode
from gpiozero import LED, Servo
import time
import pickle

laser = LED(18)
h_servo = Servo(13)
v_servo = Servo(12)

def go(h, v):
    """ Update the servo locations

    Args:
      h (float): value to set the horizontal servo to
      v (float): value to set the vertical servo to
    """
    h_servo.value = h 
    v_servo.value = v

def goslow(h, v):

    h_start = h_servo.value
    v_start = v_servo.value

    for d in range(1,101):
       h_value = h_start + (h - h_start) * (d/100.0)
       v_value = v_start + (v - v_start) * (d/100.0)
       go(h_value, v_value)
       time.sleep(0.01) 

