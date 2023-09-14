from phillips import PhillipsHue, Groups, States
from mqtt import MQTT
import time

hue = PhillipsHue()

# Callback when a message is received from the broker
def on_message(client, userdata, message):
    state = message.payload.decode()
    print(f"Setting state to {state}")

    if not hasattr(States, state):
        print("Invalid State, will default to FOCUS")
        state="FOCUS"

    hue.change_light_state(Groups.OFFICE, True, States[state])
    time.sleep(100)
    hue.change_light_state(Groups.OFFICE, False)

if __name__ == "__main__":
    mqtt = MQTT(on_message)

    mqtt.subscribe("office/lights")
    
    # Start the network loop to process incoming and outgoing messages
    mqtt.client.loop_start()

    # Keep the program running to receive messages
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting...")
        mqtt.client.disconnect()
        mqtt.client.loop_stop()
