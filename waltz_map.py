import calibrated_turret as t
import projection
import time

t.on()

for lon in range(-180, 180):
    t.go(90, lon)
    time.sleep(0.01)    

for lon in range(180, -180):
    t.go(90, lon)
    time.sleep(0.01)    

