from umqtt.simple import MQTTClient
import ubinascii
import json
import machine
import neopixel
import wifi

# MQTT Server Parameters
MQTT_BROKER = "broker.hivemq.com"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
#MQTT_TOPIC = b"com.mampersat/neopixel/1"
MQTT_TOPIC = b"com/mampersat/mousecoords"

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

def map_value(value, in_min, in_max, out_min, out_max):
    # Map value from the input range [in_min, in_max] to the output range [out_min, out_max]
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Callback when a message is received
def sub_cb(topic, msg):
    payload_dict = json.loads(msg)
    x = payload_dict['x']
    y = payload_dict['y']

    np[1] = (x, y, 0)
    np.write()

    # Map x and y to servo_x and servo_y positions
    servo_x_mapped = map_value(x, x_min, x_max, servo_x_left, servo_x_right)
    servo_y_mapped = map_value(y, y_min, y_max, servo_y_top, servo_y_bottom)            
    
    print(f'tracking to {servo_x_mapped}, {servo_y_mapped}')
    servo_x.duty_ns(servo_x_mapped)
    servo_y.duty_ns(servo_y_mapped)


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

# Run the MQTT subscription
mqtt_subscribe()