import os
import asyncio
from kasa import SmartBulb
from smart_device import SmartDevice


class Kasa(SmartDevice):
    def __init__(self, address=""):
        self.device = SmartBulb(os.environ.get("KASA_BULB_IP", address))

    async def change_state(self, group, on, brightness=50):
        await self.device.update()
        if on:
            try:
                await self.device.turn_on()
                await self.device.set_brightness(brightness)
            except:
                print("Failed to update device")
        else:
            await self.device.turn_off()


# if __name__ == "__main__":
#     try:
#         bulb = Kasa()
#         asyncio.run(bulb.change_state(True))
#     except:
#         print("Failed to update state")
