from umqtt.simple import MQTTClient
import ubinascii
import json
import machine
import neopixel
import wifi
import time

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

mapping_dict = {}

def save_mapping_dict():
    with open('mapping_dict.json', 'w') as f:
        json.dump(mapping_dict, f)

def read_mapping_dict():
    try:
        with open('mapping_dict.json', 'r') as f:
            mapping_dict = json.load(f)
    except:
        mapping_dict = {}
    return mapping_dict

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

    mouse_x = payload_dict['x']
    mouse_y = payload_dict['y']
    map_x = payload_dict['image_x']
    map_y = payload_dict['image_y']
    # add new mapping to mapping dict
    new_mapping = {(mouse_x, mouse_y): (map_x, map_y)}

    print(f'new mapping: {new_mapping}')
    mapping_dict.update(new_mapping)

def find(msg):
    payload_dict = json.loads(msg)
    mouse_x = payload_dict['x']
    mouse_y = payload_dict['y']

    # Collect distances and their corresponding mappings
    distances = []
    for key, value in mapping_dict.items():
        distance = ((value[0] - mouse_x)**2 + (value[1] - mouse_y)**2)**0.5
        distances.append((distance, key))

    # Sort by distance and take the two closest
    distances.sort(key=lambda x: x[0])
    closest_two = distances[:2]

    # goto closest point
    print(distances)
    closest = distances[0]
    print(closest)
    x = closest[1][0]
    y = closest[1][1]
    goto(json.dumps({'x': x, 'y': y}))

    
    # Extrapolate by calculating the midpoint between the two closest points
    midpoint_x = (mapping_dict[closest_two[0][1]][0] + mapping_dict[closest_two[1][1]][0]) / 2
    midpoint_y = (mapping_dict[closest_two[0][1]][1] + mapping_dict[closest_two[1][1]][1]) / 2

    print(f'Extrapolated point: ({midpoint_x}, {midpoint_y})')
    goto(json.dumps({'x': midpoint_x, 'y': midpoint_y}))

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

mapping_dict = read_mapping_dict()
print(f'Loaded mapping_dict: {mapping_dict}')

# Run the MQTT subscription
mqtt_subscribe()
