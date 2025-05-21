from umqtt.simple import MQTTClient
import ubinascii
import json
import machine
import neopixel
import wifi
import time
import random

# MQTT Server Parameters
MQTT_BROKER = "broker.hivemq.com"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
#MQTT_TOPIC = b"com.mampersat/neopixel/1"
MQTT_TOPIC = b"com/mampersat/#"

laser = machine.Pin(16, machine.Pin.OUT)
laser.on()

np = neopixel.NeoPixel(machine.Pin(28), 5)
servo_x = machine.PWM(machine.Pin(17), freq=50)
servo_y = machine.PWM(machine.Pin(18), freq=50)

# Servo x configuration
servo_x_left = 3_000_000
servo_x_right = 600_000
x_min = 0
x_max = 1000

# Servo y configuration
servo_y_top = 600_000
servo_y_bottom = 3_000_000
y_min = 0
y_max = 1000

#######################################
## New data structure to store mappings
#######################################

# Define a dictionary to store the mappings
coordinate_mappings = {
    "laser_to_image": {},
    "image_to_laser": {}
}

def add_mapping(laser_x, laser_y, image_x, image_y):
    coordinate_mappings["laser_to_image"][(laser_x, laser_y)] = (image_x, image_y)
    coordinate_mappings["image_to_laser"][(image_x, image_y)] = (laser_x, laser_y)

def get_image_from_laser(laser_x, laser_y):
    return coordinate_mappings["laser_to_image"].get((laser_x, laser_y))

def get_laser_from_image(image_x, image_y):
    return coordinate_mappings["image_to_laser"].get((image_x, image_y))


def find(msg):
    """ Find the closest image point and navigate to the laser point"""
    payload_dict = json.loads(msg)
    image_x = payload_dict['x']
    image_y = payload_dict['y']

    # goto the first position
    d = coordinate_mappings["image_to_laser"]
    r = random.choice(list(d.items()))

    # find closest point in image_to_laser
    min_distance = 1000000
    for k, v in d.items():
        # pull x and y out of the key which is a string
        x, y = map(float, k.strip('[]').split(', '))
        distance = (image_x - x)**2 + (image_y - y)**2
        if distance < min_distance:
            min_distance = distance
            r = v

    print(r)
    print(f'min_distance={min_distance}')
          
    # Navigate to the found laser point
    goto(json.dumps({"x": int(r[0]), "y": int(r[1])}))

def save_coordinate_mappings():
    with open('coordinate_mappings.json', 'w') as f:
        json.dump(coordinate_mappings, f)

def clear_coordinate_mappings():
    global coordinate_mappings
    coordinate_mappings = {
        "laser_to_image": {},
        "image_to_laser": {}
    }
    save_coordinate_mappings()

def read_coordinate_mappings():
    try:
        with open('coordinate_mappings.json', 'r') as f:
            coordinate_mappings = json.load(f)
    except:
        coordinate_mappings = {
           "laser_to_image": {},
            "image_to_laser": {}
        }
    return coordinate_mappings

def map_value(value, in_min, in_max, out_min, out_max):
    # Map value from the input range [in_min, in_max] to the output range [out_min, out_max]
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Callback when a message is received
def sub_cb(topic, msg):
    np[0] = (0,50,0)
    print(f'topic={topic}')
    print(f'msg={msg}')
    if topic == b'com/mampersat/laser/goto':
        goto(msg)
    
    if topic == b'com/mampersat/laser/map':
        map_coord(msg)

    if topic == b'com/mampersat/laser/find':
        find(msg)

    np[0] = (0,0,0)

def goto(msg):
    print(f'goto: {msg}')
    payload_dict = json.loads(msg)
    x = int(payload_dict['x'])
    y = int(payload_dict['y'])

    np[1] = (int(x), int(y), 0)
    np.write()

    # Map x and y to servo_x and servo_y positions
    servo_x_mapped = map_value(x, x_min, x_max, servo_x_left, servo_x_right)
    servo_y_mapped = servo_y_bottom - map_value(y, y_min, y_max, servo_y_top, servo_y_bottom)            
    
    print(f'tracking to {servo_x_mapped}, {servo_y_mapped}')
    servo_x.duty_ns(servo_x_mapped)
    servo_y.duty_ns(servo_y_mapped)
    

def map_coord(msg):
    payload_dict = json.loads(msg)

    laser_x = payload_dict['x']
    laser_y = payload_dict['y']
    image_x = payload_dict['image_x']
    image_y = payload_dict['image_y']

    add_mapping(laser_x, laser_y, image_x, image_y)
    save_coordinate_mappings()

# Setup MQTT Client and Subscribe
def mqtt_subscribe():
    client = MQTTClient(CLIENT_ID, MQTT_BROKER)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(MQTT_TOPIC)
    print("Connected to %s, subscribed to %s topic" % (MQTT_BROKER, MQTT_TOPIC))
    
    try:
        while True:
            client.wait_msg()  # Blocking wait for a message
    except KeyboardInterrupt:
        pass
    finally:
        client.disconnect()

coordinate_mappings = read_coordinate_mappings()
print(f'Loaded mapping_dict: {coordinate_mappings}')

# Run the MQTT subscription
mqtt_subscribe()
