import laser_turret as t
import time
import pickle

anchors = pickle.load(open("anchors.p", "rb"))

t.laser.on()

while True:
    for location in anchors:
        print(location[0])
        t.goslow(location[3], location[4])
        time.sleep(5)

