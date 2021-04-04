from haversine import haversine
import pickle

anchors = pickle.load(open("anchors.p", "rb"))

def algorythm_1(lat, lon):
    """ Estimate and navigate to lat lon 

    Find two closest anchors and extrapolate on line between them

    args:
        lat: lattitude
        lon: longitue
    """
    sorted_tuples = sorted(anchors.items(), key=lambda item: haversine( (lat, lon), (item[1][0], item[1][1]) ))
    
    # two closest anchors
    p1 = sorted_tuples[0][1]
    p2 = sorted_tuples[1][1]

    # distance to closest 2
    d1 = haversine( (lat, lon), (p1[0], p1[1]))
    d2 = haversine( (lat, lon), (p2[0], p2[1]))

    # ratio of distance from point 1 to point 2
    ratio = d1 / d2

    h = p1[2] + (p2[2] - p1[2] ) * ratio
    v = p1[3] + (p2[3] - p1[3] ) * ratio

    return h,v

    