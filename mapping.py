import math
import uos
import json



def write_starter_data():
    map_data = {
        'world': [ # map_id
            {
                'lat': 0,
                'long': 0,
                'coordinates': (1795200, 1502400)
            },
            {
                'lat': 90,
                'long': 0,
                'coordinates': (1759200, 1339200)
            },
            {
                'lat': 90,
                'long': -180,
                'coordinates': (1951200, 1308000)
            },
            {
                'lat': 0,
                'long': -180,
                'coordinates': (2196000, 1516800)
            },
        ],
    }

    data_str = json.dumps(map_data)

    # Write the JSON string to a file
    with open('/data.json', 'w') as file:
        file.write(data_str)

def read_data():
    with open('/data.json', 'r') as file:
        data_str = file.read()
        data = json.loads(data_str)
    return data        