import asyncio
from kasa import SmartBulb
from smart_device import SmartDevice, States


class TpLinkHandler(SmartDevice):
    def __init__(self, logger, address):
        super().__init__(logger)
        self.device = SmartBulb(address)
        self.loop = asyncio.get_event_loop()

    def shutdown(self):
        asyncio.run_coroutine_threadsafe(self.device.turn_off(), self.loop)

    def turn_on(self, state: States):
        # super().turn_on(state)
        asyncio.run_coroutine_threadsafe(self.device.turn_on(), self.loop)
        self.set_brightness(state.value)

    def set_brightness(self, num: int):
        self.log.info(f"Setting light to {num}%")
        asyncio.run_coroutine_threadsafe(self.device.set_brightness(num), self.loop)
        asyncio.run_coroutine_threadsafe(self.device.update(), self.loop)

    def __repr__(self):
        return self.details
