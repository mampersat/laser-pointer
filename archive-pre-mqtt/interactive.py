import requests
import spacy
import api_keys
import laser_turret
import projection
import time
import os


def get_location(input: str):
    """ Query maps api with string 

    Args:
        input: A string, usually an article title, to try to get a location for

    Returns:
        tuple: name, lat, lng
        -or- None if error/no results

    """
    maps_api_url ='https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=' + input
    maps_api_url += '&inputtype=textquery&fields=name,geometry&key=' + api_keys.google_maps_key
    # return maps_api_url
    r = requests.get(maps_api_url)
    try:
        name = r.json()['candidates'][0]['name']
        lat = r.json()['candidates'][0]['geometry']['location']['lat']
        lng = r.json()['candidates'][0]['geometry']['location']['lng']
        return(name, lat, lng)
        return r
    except:
        return None

nlp = spacy.load('en_core_web_sm')

laser_turret.laser.on()

while True:
    s = input()
    print(f'input: {s}')

    ents = nlp(s).ents
    location = None
    if len(ents):
        location_string = str(ents[0])
        location = get_location(location_string)

    if location:
        print(f'anchors["{location[0]}"] = ({location[1]},{location[2]})')
        h,v = projection.algorythm_1(location[1],location[2])
        laser_turret.go(h,v)
