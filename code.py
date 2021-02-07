# Imports
import time
from secrets import secrets


def main():
    # Setup
    magtag.peripherals.neopixel_disable = False
    magtag.peripherals.neopixels.fill((100, 0, 100))
    # Loop
    while True:
        if magtag.peripherals.buttons[0]:
            magtag.peripherals.neopixels.fill((0, 100, 100))
        response = requests.get(
            secrets["endpoint"] + "/api/stock",
            headers={
                "GROCY-API-KEY": secrets["api_key"],
                "accept": "application/json",
            },
        )
        raise Exception(response.text)
        time.sleep(0.01)
