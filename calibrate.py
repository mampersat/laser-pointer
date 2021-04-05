import laser_turret as t
import os.path
import pickle
import os.path
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

defaults = {'null': (0,0),
         'west': (-90,0),
         'north': (0, 90),
         'east': (90, 0),
         'south': (0, -90)
         }


# Draw a circle around London
t.laser.on()

if os.path.exists('anchors.p'):
    anchors = pickle.load(open("anchors.p", "rb"))
else:
    anchors = defaults

# add additional anchors - should be needed often
# anchors['London'] = (51.5075, -0.1278)
# anchors['Washington DC'] =  (38.9072, -77.0369)
# anchors['Brasilia'] = (-15.8267, -47.9218)
# anchors['Honolulu'] = (21.3069, -157.8583)
# anchors['Brisbane'] = (-27.47, 153.0260)
# anchors['Juneau'] = (58.3019, -134.4197)
# anchors['Delhi'] = (28.7041, 77.1025)
anchors['Antananaviro'] = (-18.8792, 47.5079)

def project_from_lat_lon(lat, lon):
    """ Use exsiting anchors to extrapolate to turret coord """
    # Find 2 closest known points
    # Calculate h as spot along east->west line
    x1 = anchors['west'][0]
    y1 = anchors['west'][1]

    x2 = anchors['east'][0]
    y2 = anchors['west'][1]

    n = anchors['west'][2] 


if __name__ == "__main__":

    print("Use w,a,s,d keys to move pointer. W = reverse horizonal direction, A = reverse vertical direction.")

    for anchor_key in anchors:  #anchors.iterkeys(): # range(len(anchors)): #anchor in anchors:
        coords = anchors[anchor_key]

        if len(coords) > 2:
            h,v = coords[2], coords[3]
        else:
            h, v = lat_lon_to_turret(coords[0], coords[1])
        t.go(h, v)

        print("Turret callibration.for location: ------>", anchor_key, coords)
        # My device is wired so horizonal is backwards... so neg here
        hd = -0.01 # Horizontal Driver
        vd = 0.01 # Vertical Driver

        written = False
        while not written:
            t.go(h, v)
            value = input("use w/a/s/d keys to adjust:\n")
            if value == 'A':
                h -= hd *10
            if value=='a':
                h -= hd
            if value == 'd':
                h += hd
            if value == 'D':
                h += hd *10

            if value =='W':
                v -= vd*10
            if value =='w':
                v -= vd
            if value =='s':
                v += vd
            if value =='S':
                v += vd*10

            if value =='p':
                anchors[anchor_key] = anchors[anchor_key][0:2]+ (h, v)
                pickle.dump(anchors, open("anchors.p", "wb"))
                written = True

            if value =='x':
                written = True
