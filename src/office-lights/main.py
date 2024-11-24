from phillips import PhillipsHue, Groups, States
from mqtt import MQTT
import time

hue = PhillipsHue()
IS_DISABLED = False


# Callback when a message is received from the broker
def on_message(client, userdata, message):
    global IS_DISABLED
    state = message.payload.decode()

    # Disable/enable office lights
    if state == "DISABLE" or state == "ENABLE":
        hue.change_light_state(Groups.OFFICE, False)
        IS_DISABLED = state == "DISABLE"
        print(f"Motion Disabled: {IS_DISABLED}")
        return

    if not IS_DISABLED:
        print(f"Setting state to {state}")

        if state == "OFF":
            hue.change_light_state(Groups.OFFICE, False)
            return

        if not hasattr(States, state):
            print("Invalid State, will default to FOCUS")
            state = "FOCUS"

        hue.change_light_state(Groups.OFFICE, True, States[state])


if __name__ == "__main__":
    try:
        mqtt = MQTT(on_message)

        mqtt.subscribe("office/lights")

        # Start the network loop to process incoming and outgoing messages
        mqtt.client.loop_start()
    except Exception:
        print("MQTT Configuration failed")

    try:
        # Keep the program running to receive messages
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        mqtt.client.disconnect()
        mqtt.client.loop_stop()
