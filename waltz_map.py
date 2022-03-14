import calibrated_turret as t
import projection
import time

t.on()

for lon in range(-180, 180):
    t.go(0, lon)
    print(lon)
    time.sleep(0.1)    

for lat in range(-90, 90):
    t.go(lat, 0)
    time.sleep(0.1)    

