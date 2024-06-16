import time
from umqtt.simple import MQTTClient
import ubinascii
import json
import machine
import neopixel

# MQTT Server Parameters
MQTT_BROKER = "broker.hivemq.com"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
#MQTT_TOPIC = b"com.mampersat/neopixel/1"
MQTT_TOPIC = b"com/mampersat/mousecoords"

np = neopixel.NeoPixel(machine.Pin(28), 5)

# Callback when a message is received
def sub_cb(topic, msg):
    print((topic, msg))
    payload_dict = json.loads(msg)
    x = payload_dict['x']
    y = payload_dict['y']
    np[1] = (x, y, 0)
    np.write()
            



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
