// mqttHandler.js

// MQTT Broker details
const MQTT_BROKER = "broker.hivemq.com";
const MQTT_PORT = 8884;
const MQTT_TOPIC = "com/mampersat/mousecoords";

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
    message.destinationName = MQTT_TOPIC;
    client.send(message);
}
