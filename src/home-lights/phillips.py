import requests
from enum import Enum
import os
from smart_device import SmartDevice, States


class PhillipsHue(SmartDevice):
    def __init__(self, logger, address=""):
        super().__init__(logger)
        if (
            "HUE_BRIDGE_ADDRESS" not in os.environ
            or "HUE_BRIDGE_USERNAME" not in os.environ
        ):
            raise EnvironmentError(
                f"The environment variable 'HUE_BRIDGE_ADDRESS' or 'HUE_BRIDGE_USERNAME is not set."
            )

        address = os.environ.get("HUE_BRIDGE_ADDRESS")
        self.api = f"http://{address}/api"
        self.username = os.environ.get("HUE_BRIDGE_USERNAME")

    def turn_on(self, state=States.FOCUS):
        super().turn_on(state)
        data = {
            "on": True,
        }
        data.update(state.value)

        response = requests.put(
            f"{self.api}/{self.username}/groups/1/action", json=data
        )

        if response.status_code == 200:
            self.log.info("POST request successful")
            self.log.info(f"Response: {response.text}")
        else:
            self.log.info("POST request failed with status code:", response.status_code)

    def turn_off(self):
        data = {
            "on": False,
        }

        response = requests.put(
            f"{self.api}/{self.username}/groups/1/action", json=data
        )

        if response.status_code == 200:
            self.log.info("POST request successful")
            self.log.info(f"Response: {response.text}")
        else:
            self.log.info("POST request failed with status code:", response.status_code)


if __name__ == "__main__":
    hue = PhillipsHue()
    # hue.change_state(Groups.OFFICE, True, States.ALERT)
