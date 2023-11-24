import os
import asyncio
from kasa import SmartBulb
from smart_device import SmartDevice


class Kasa(SmartDevice):
    def __init__(self, address=""):
        self.device = SmartBulb(os.environ.get("KASA_BULB_IP", address))
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def __del__(self):
        # Destructor: Close the event loop when the object is about to be destroyed
        if hasattr(self, "loop") and self.loop.is_running():
            self.loop.stop()
        self.loop.close()

    async def change_state(self, group, on, brightness):
        await self.device.update()
        if on:
            try:
                await self.device.turn_on()
                await self.device.set_brightness(int(brightness))
            except Exception as e:
                print(f"Failed to update device {e}")
        else:
            await self.device.turn_off()


# if __name__ == "__main__":
#     try:
#         bulb = Kasa()
#         asyncio.run(bulb.change_state(True))
#     except:
#         print("Failed to update state")
