import time
import threading
import logging


class DeviceTimer:
    def __init__(self):
        self.timeout = 300
        self.active_timer = None

    def new_timer(self, callback):
        logging.info("Resetting activity timer")
        # Cancel any active timers
        self.cancel()
        self.active_timer = threading.Timer(self.timeout, lambda: callback())

    def start(self):
        self.active_timer.start()

    def cancel(self):
        if self.active_timer:
            self.active_timer.cancel()
