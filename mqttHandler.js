// mqttHandler.js

// MQTT Broker details
const MQTT_BROKER = "broker.hivemq.com";
const MQTT_PORT = 8884;
const MQTT_TOPIC_GOTO = "com/mampersat/laser/goto";
const MQTT_TOPIC_MAP = "com/mampersat/laser/map";
const MQTT_TOPIC_FIND = "com/mampersat/laser/find";

// Create a client instance
const clientID = "mqtt_js_" + Math.random().toString(16).substr(2, 8);
const client = new Paho.Client(MQTT_BROKER, MQTT_PORT, clientID);

// Set callback handlers
client.onConnectionLost = function (responseObject) {
    if (responseObject.errorCode !== 0) {
        console.log("onConnectionLost:", responseObject.errorMessage);
    }
};

client.onMessageArrived = function (message) {
    console.log("onMessageArrived:", message.payloadString);
};

// Connect the client
client.connect({
    onSuccess: onConnect,
    useSSL: true
});

// Called when the client connects
function onConnect() {
    console.log("Connected to MQTT broker");
}

// Send mouse coordinates over MQTT
// x = 0 -> 1000
// y = 0 -> 1000
function sendMouseCoords(x, y) {
    const message = new Paho.Message(JSON.stringify({ x: x, y: y }));
    message.destinationName = MQTT_TOPIC_GOTO;
    client.send(message);
}

// Send mapping coordinates over MQTT
function sendMappingCoords(mapping) {
    const message = new Paho.Message(JSON.stringify(mapping));
    message.destinationName = MQTT_TOPIC_MAP;
    client.send(message);
}

// Send find coordinates over MQTT
function sendFindCoords(find) {
    const message = new Paho.Message(JSON.stringify(find));
    message.destinationName = MQTT_TOPIC_FIND;
    client.send(message);
}
