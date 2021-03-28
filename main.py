from gpiozero import LED, Servo
import time

laser = LED(18)
h_servo = Servo(13)
v_servo = Servo(12)

locations = [
    (-1.0, 0.068, 'home_bowmap'),
    (0.44, -0.1, 'boston'),
    (-0.04, 0.076, 'myanmar'),
    (0.148, -0.0, 'suez'),
    (0.9, 0.08, -180, 0),
    (-0.212, 0.16, 180, 0),
    # (0.86, -0.32, 'top left'),
    # (-0.212, -0.152, 'top right'),
]

def go(location):

    h_servo.value = location[0]
    v_servo.value = location[1]

def goslow(location):

    h_start = h_servo.value
    v_start = v_servo.value

    for d in range(1,101):
       h_servo.value = h_start + (location[0] - h_start) * (d/100.0)
       v_servo.value = v_start + (location[1] - v_start) * (d/100.0)
       time.sleep(0.01) 

laser.on()
h_servo.value = 0
v_servo.value = 0

while True:
    for location in locations:
	goslow(location)
        print(location[2])
        time.sleep(1)

