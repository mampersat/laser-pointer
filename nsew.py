import laser_turret as t
import time
import pickle

anchors = pickle.load(open("anchors.p", "rb"))

t.laser.on()

while True:
    for key in ('null', 'north', 'south', 'east', 'west'):
        print(key)

        
        
        t.goslow(anchors[key][2], anchors[key][3])
        time.sleep(1)

