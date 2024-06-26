import laser_turret as t
import projection as p

def go(lat, lon):
    point = p.algorythm_3(lat, lon)
    t.go(point[0], point[1])

def on():
    t.laser.on()

def off():
    t.laser.off()