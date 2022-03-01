from haversine import haversine
import pickle
import os

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
    """ Estimate and navigate to lat lon 

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

    return v,h

    
