import requests
from enum import Enum
import os

class States(Enum):
    FOCUS = {"bri": 254, "hue": 10000, "sat": 101,}
    ALERT = {"bri": 254, "hue": 2, "sat": 140,}

class Groups(Enum):
    OFFICE = 1

class PhillipsHue:
    def __init__(self):
        if "HUE_BRIDGE_ADDRESS" not in os.environ or "HUE_BRIDGE_USERNAME" not in os.environ:
            raise EnvironmentError(f"The environment variable 'HUE_BRIDGE_ADDRESS' or 'HUE_BRIDGE_USERNAME is not set.")
        
        address = os.environ.get("HUE_BRIDGE_ADDRESS")
        self.api = f"http://{address}/api"
        self.username = os.environ.get("HUE_BRIDGE_USERNAME")


    def change_light_state(self, group: Groups, on=False, mode=States.FOCUS):
        data = {
            "on": on,
        }

        if not isinstance(mode, States):
            print("Invalid mode, will not set lighting states")
        elif on:
            data.update(mode.value)
        
        response = requests.put(f"{self.api}/{self.username}/groups/{group.value}/action", json=data)

        if response.status_code == 200:
            print("POST request successful")
            print("Response:", response.text)
        else:
            print("POST request failed with status code:", response.status_code)

if __name__ == "__main__":
    hue = PhillipsHue()
    hue.change_light_state(Groups.OFFICE, True, States.ALERT)
