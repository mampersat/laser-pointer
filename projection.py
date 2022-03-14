from haversine import haversine
import pickle
import os

# todo remove - just debugging
import laser_turret as t
import time

if os.path.exists('anchors.p'):
    anchors = pickle.load(open("anchors.p", "rb"))
else:
    anchors = {'null': (0, 0, 0, 0),
         'west': (-90, 0,-90, 0),
         'north': (0, 90, 0, 90),
         'east': (90, 0, 90, 0),
         'south': (0, -90, 0, -90)
         }

def algorythm_1(lat, lon):
    """ Estimate h and v based on anchors

    Find two closest anchors and extrapolate on line between them

    args:
        lat: lattitude
        lon: longitue
    """
    # Only use anchors with projections
    calibrated_anchors = {k:v for (k,v) in anchors.items() if len(v)> 2}
    sorted_tuples = sorted(calibrated_anchors.items(), key=lambda item: haversine( (lat,lon), (item[1][0], item[1][1])))
    
    # two closest anchors
    p1 = sorted_tuples[0][1]
    p2 = sorted_tuples[1][1]

    # distance to closest 2
    d1 = haversine( (lat, lon), (p1[0], p1[1]))
    d2 = haversine( (lat, lon), (p2[0], p2[1]))

    # ratio of distance from point 1 to point 2
    ratio = d1 / (d1 + d2)

    v = p1[2] + (p2[2] - p1[2] ) * ratio
    h = p1[3] + (p2[3] - p1[3] ) * ratio

    # todo debug code remove
    """
    t.laser.on()
    t.go(p1[2], p1[3])
    time.sleep(0.5)
    t.go(p2[2], p2[3])
    time.sleep(0.5)
    t.go(v, h)
    """

    return v,h

def algorythm_2(lat, lon):
    """ Estimate h and v based on anchors

    Find closest anchor, calculate ratio of v to lat and h to lon and apply

    args:
        lat: lattitude
        lon: longitue
    """
    # Only use anchors with projections
    calibrated_anchors = {k:v for (k,v) in anchors.items() if len(v)> 2}
    sorted_tuples = sorted(calibrated_anchors.items(), key=lambda item: haversine( (lat,lon), (item[1][0], item[1][1])))
    
    # closest anchors
    p = sorted_tuples[0][1]

    origin = anchors['null']

    # ratio of distance from point 1 to point 2
    if (p == origin):
        vratio = 1
        hratio = 1
    else:
        vratio = ( origin[2] - p[2] ) / (p[0] - origin[0])
        hratio = ( origin[3] - p[3] ) / (p[1] - origin[1])

    v = origin[2] + lat * vratio
    h = origin[3] + lon * hratio

    # todo debug code remove
    """
    t.laser.on()
    t.go(p1[2], p1[3])
    time.sleep(0.5)
    t.go(p2[2], p2[3])
    time.sleep(0.5)
    t.go(v, h)
    """

    return v,h    

def algorythm_3(lat, lon):
    """ Estimate h and v based on anchors

    Same as algorythm_1, but use closest point and origin ('null island')

    args:
        lat: lattitude
        lon: longitue
    """
    # Only use anchors with projections
    calibrated_anchors = {k:v for (k,v) in anchors.items() if len(v)> 2}
    sorted_tuples = sorted(calibrated_anchors.items(), key=lambda item: haversine( (lat,lon), (item[1][0], item[1][1])))
    
    # two closest anchors
    p2 = sorted_tuples[0][1]
    p1 = anchors['null']

    # if the closest point is origin, use next two
    if (p2 == p1):
        p2 = sorted_tuples[1][1]

    print(f'Closest anchor {sorted_tuples[0][0]}')
    # distance to closest 2
    d1 = haversine( (lat, lon), (p1[0], p1[1]))
    d2 = haversine( (lat, lon), (p2[0], p2[1]))

    # ratio of distance from point 1 to point 2
    if (d1 + d2 ==0):
        ratio = 0
    else:
        ratio = d1 / (d1 + d2)

    v = p1[2] + (p2[2] - p1[2] ) * ratio
    h = p1[3] + (p2[3] - p1[3] ) * ratio

    # todo debug code remove
    """
    t.laser.on()
    t.go(p1[2], p1[3])
    time.sleep(0.25)
    t.go(p2[2], p2[3])
    time.sleep(0.25)
    t.go(v, h)
    """

    return v,h    
