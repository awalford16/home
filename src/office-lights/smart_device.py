from abc import ABC, abstractmethod
from enum import Enum


class Groups(Enum):
    OFFICE = 1
    LIVING_ROOM = 2


class SmartDevice(ABC):
    @abstractmethod
    def change_state(self, group: Groups, on: bool, state):
        pass
