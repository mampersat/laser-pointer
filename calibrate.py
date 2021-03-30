import laser_turret as t
import pickle
import time

def lat_lon_to_turret(lat, lon):
    """ Convert latitude and longitude to turret coordinates

    Args:
        lat: Lattitude
        lon: Longiture

    Returns:
        h (float): horizontal servo value
        v (float) : vertical servo value"""

    # get working without callibration
    h = float(lat) / 180 
    v = float(lon) / 180
    return h,v

def turret_to_lat_lon(h, v):
    """ Convert turret coordinates to lattitude and longiture

    Args:
        h: horontal servo value
        v: vertical servo value

    Returns:
        lat: latitude
        lon: longitude
    """
    lat = float(h) * 180 
    lon = float(v) * 180
    return lat, lon

def write_defaults():
    """ Initalize the calibration pickle with reasonable values """

    anchors = [
            ('null island', 0, 0),
            # ('London', 51.5075, -0.1278),
            # ('Washington DC', 38.9072, -77.0369),
            # ('Brasilia', -15.8267, -47.9218),
            ('West', -90, 0),
            ('North', 0, 90),
            ('East', 90, 0),
            ('South', 0, -90)
    ]

    pickle.dump(anchors, open("anchors.p", "wb"))


# Draw a circle around London
t.laser.on()

anchors = pickle.load(open("anchors.p", "rb"))

print("Use w,a,s,d keys to move pointer. W = reverse horizonal direction, A = reverse vertical direction.")

for anchor_index in range(len(anchors)): #anchor in anchors:
    anchor = anchors[anchor_index]

    h, v = lat_lon_to_turret(anchor[1], anchor[2])
    t.go(h, v)

    print("Turret callibration.for location:", anchor[0])
    hd = 0.01 # Horizontal Driver
    vd = 0.01 # Vertical Driver

    written = False
    while not written:
        t.go(h, v)
        value = raw_input("use w/a/s/d keys to adjust:\n")
        print(value)
        if value == 'A':
            hd = - hd
        if value=='a':
            h -= hd
        if value == 'd':
            h += hd

        if value =='W':
            vd = -vd
        if value =='w':
            v -= vd
        if value =='s':
            v += vd

        if value =='p':
            anchors[anchor_index] += (h, v)
            pickle.dump(anchors, open("anchors.p", "wb"))
            written = True

