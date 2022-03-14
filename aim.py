import calibrated_turret as ct
import time

while True:
    ct.go(0,0)
    ct.on()
    time.sleep(1)
    ct.go(150,0)
    time.sleep(1)
    ct.go(-150,0)
    time.sleep(1)
    ct.go(90,0)
    time.sleep(1)
    ct.go(-90,0)
    time.sleep(1)
