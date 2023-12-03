import paho.mqtt.client as mqtt


# Callback when the client publishes a message
def on_publish(client, userdata, mid):
    print("Message published")


# Create an MQTT client instance
client = mqtt.Client()

# Set the callback for publishing
client.on_publish = on_publish

# Set the broker address and port
broker_address = "192.168.0.120"  # Replace with your broker's address
port = 1883  # Default MQTT port

# Connect to the broker
client.connect(broker_address, port)

# Start the network loop to process outgoing messages
client.loop_start()

# Publish a message to a topic
topic = "office/lights"  # Replace with the topic you want to publish to
message = "FOCUS"  # Your message here
# client.publish(topic, message)
# client.publish(topic, "ALERT")
# client.publish(topic, message)
# client.publish(topic, "INVALID")
client.publish(topic, message)

# Wait for a moment to allow the message to be sent
client.loop_stop()
