import laser_turret as t
import time
import pickle
import projection as p

anchors = pickle.load(open("anchors.p", "rb"))

t.go(0,0)
t.laser.on()

while True:
    for key in anchors:
        print(key, anchors[key])
       
        if len(anchors[key]) ==4 :
            t.goslow(anchors[key][2], anchors[key][3])
        else:
            # print(f'Uncalibrated anchor {key}')
            hav = p.algorythm_1(anchors[key][0], anchors[key][1]) 
            t.goslow(hav[0], hav[1])

        time.sleep(1)

