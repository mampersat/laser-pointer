import laser_turret as t
import time
import pickle

anchors = pickle.load(open("anchors.p", "rb"))

t.laser.on()

while True:
    for key in anchors:
        print(key, anchors[key])
       
        if len(anchors[key]) ==4 :
            t.goslow(anchors[key][2], anchors[key][3])
        else:
            print(f'Uncalibrated anchor {key}')
        time.sleep(1)

