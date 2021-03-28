import laser_turret as t
import time

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

t.laser.on()

while True:
    for location in locations:
	# goslow(location[0], location[1])
        t.goslow(location[0], location[1])
        print(location[2])
        time.sleep(5)

