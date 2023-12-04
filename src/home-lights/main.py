from tplink import TpLinkHandler
from enum import Enum
import logging
import asyncio
from phillips import PhillipsHue
import asyncio_mqtt as aiomqtt
from smart_device import States
import os

FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Topics(Enum):
    LIVING_ROOM = "lounge/lights"
    OFFICE = "office/lights"


MQTT_SERVER = os.environ.get("MQTT_ADDRESS", "")
TPLINK_BULB_IP = os.environ.get("KASA_BULB_IP", "")


async def main():
    handlers = {
        "lounge/lights": TpLinkHandler(logger, TPLINK_BULB_IP),
        "office/lights": PhillipsHue(logger),
    }
    while True:
        try:
            async with aiomqtt.Client(MQTT_SERVER) as client:
                logger.info(f"Connected to MQTT Server: {client._connected.result()}")

                async with client.messages() as messages:
                    await client.subscribe(Topics.LIVING_ROOM.value)
                    await client.subscribe(Topics.OFFICE.value)

                    async for message in messages:
                        logger.info(
                            f"Setting {message.topic.value} to {message.payload.decode('utf-8')}"
                        )
                        try:
                            if message.payload == b"OFF":
                                handlers[message.topic.value].turn_off()
                            else:
                                handlers[message.topic.value].turn_on(
                                    States[message.payload.decode("utf-8")]
                                )
                        except Exception as e:
                            handlers[message.topic.value].log.error(
                                f"Failed to update: {e}"
                            )
        except Exception as e:
            logger.error(f"MQTT Connection error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
