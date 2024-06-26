import laser_turret as t
import calibrated_turret as ct
import projection as p
t.laser.on()

import pickle
anchors = pickle.load(open("anchors.p", "rb"))
print('When done, run\npickle.dump(anchors, open("anchors.p", "wb"))')

