from phillips import PhillipsHue, States
from tplink import Kasa
from mqtt import MQTT
from enum import Enum
from smart_device import Groups
import logging
import asyncio

hue = PhillipsHue()

FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Topics(Enum):
    LIVING_ROOM = "lounge/lights"
    OFFICE = "office/lights"


# Callback when a message is received from the broker
def on_message(client, userdata, message):
    state = message.payload.decode()
    logger.info(f"Setting state to {state} for {message.topic}")
    is_off = state == "OFF"

    if message.topic == Topics.LIVING_ROOM.value:
        # state in this context refers to bulb brightness
        kasa = Kasa()
        asyncio.run(kasa.change_state(Groups.LIVING_ROOM.value, not is_off, state))
    elif message.topic == Topics.OFFICE.value:
        # Will ignore state if set to off
        hue.change_state(Groups.OFFICE.value, not is_off, getattr(States, state, None))


if __name__ == "__main__":
    try:
        mqtt = MQTT(logger, on_message)

        mqtt.subscribe("office/lights")
        mqtt.subscribe("lounge/lights")

        logger.info("Subscribed")

        # Start the network loop to process incoming and outgoing messages
        mqtt.client.loop_start()
    except Exception as e:
        logger.error(f"MQTT Configuration failed: {e}")

    try:
        # Keep the program running to receive messages
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("Exiting...")
        exit(0)
    finally:
        mqtt.client.disconnect()
        mqtt.client.loop_stop()
