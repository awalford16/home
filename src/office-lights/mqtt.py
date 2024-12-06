import paho.mqtt.client as mqtt
from timer import DeviceTimer
from constants import MQTT_SERVER
import os
import sys


class MQTT:
    def __init__(self, on_message):
        # Create an MQTT client instance
        self.client = mqtt.Client()

        # Set the callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = on_message

        # Set the broker address and port
        if "MQTT_ADDRESS" not in os.environ:
            raise EnvironmentError(
                f"The environment variable 'MQTT_ADDRESS' is not set."
            )

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


#########################
# TESTING FUNCTIONALITY #
#########################
def test_on_publish(client, userdata, mid):
    print("Message published")


def test_on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


TEST_TOPIC = "office/test"

if __name__ == "__main__":
    # Arg parser to run tester
    # Callback when the client publishes a message

    # Create an MQTT client instance
    client = mqtt.Client()

    # Set the callback for publishing
    client.on_publish = test_on_publish
    client.on_message = test_on_message

    # Set the broker address and port
    port = 1883  # Default MQTT port

    # Connect to the broker
    client.connect(MQTT_SERVER, port)

    if sys.argv[1] == "publish":
        # Start the network loop to process outgoing messages
        client.loop_start()

        # Publish a message to a topic
        message = "OFF"  # Your message here
        # client.publish(topic, message)
        # client.publish(topic, "ALERT")
        # client.publish(topic, message)
        # client.publish(topic, "INVALID")
        client.publish(TEST_TOPIC, message)

        # Wait for a moment to allow the message to be sent
        client.loop_stop()
    else:
        client.subscribe(TEST_TOPIC)
        # Start the network loop to process outgoing messages
        client.loop_forever()
