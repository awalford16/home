from abc import ABC, abstractmethod
from enum import Enum


class Groups(Enum):
    OFFICE = "1"
    LIVING_ROOM = "2"


class States(Enum):
    FOCUS = {
        "bri": 254,
        "hue": 10000,
        "sat": 101,
    }
    ALERT = {
        "bri": 254,
        "hue": 2,
        "sat": 140,
    }
    # Brightness states for TPLink
    RELAX = 5
    READ = 20


class SmartDevice:
    def __init__(self, logger, address=""):
        self.log = logger
        # self.connect()

    def turn_on(self, state: States):
        if not isinstance(state, States):
            self.log.info("Invalid state, will not set lighting states")
            return

        self.log.info(f"Setting state to {state}")

    def turn_off(self):
        pass
