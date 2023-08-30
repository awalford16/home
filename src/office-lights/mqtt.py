import paho.mqtt.client as mqtt
import os

class MQTT():
    def __init__(self, on_message):
        # Create an MQTT client instance
        self.client = mqtt.Client()

        # Set the callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = on_message

        # Set the broker address and port
        if "MQTT_ADDRESS" not in os.environ:
            raise EnvironmentError(f"The environment variable 'MQTT_ADDRESS' is not set.")

        broker_address = os.environ.get("MQTT_ADDRESS")
        port = 1883  # Default MQTT port

        # Connect to the broker
        self.client.connect(broker_address, port)

    def subscribe(self, topic):
        self.client.subscribe(topic)

    # Callback when the client receives a CONNACK response from the broker
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
        else:
            print("Connection failed with code", rc)

