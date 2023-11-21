from phillips import PhillipsHue, States
from tplink import Kasa
from mqtt import MQTT
from enum import Enum
from smart_device import Groups

hue = PhillipsHue()
kasa = Kasa()


class Topics(Enum):
    LOUNGE = "lounge/lights"
    OFFICE = "office/lights"


# Callback when a message is received from the broker
def on_message(client, userdata, message):
    state = message.payload.decode()
    print(f"Setting state to {state}")
    is_off = state == "OFF"

    if message.topic == Topics.LOUNGE:
        # state in this context refers to bulb brightness
        kasa.change_state(Groups.LOUNGE, is_off, state)
    elif message.topic == Topics.OFFICE:
        # Will ignore state if set to off
        hue.change_state(Groups.OFFICE, is_off, getattr(States, state, None))


if __name__ == "__main__":
    try:
        mqtt = MQTT(on_message)

        mqtt.subscribe("office/lights")
        mqtt.subscribe("lounge/lights")

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
