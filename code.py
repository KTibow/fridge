# Imports
import time
from secrets import secrets


def main():
    # Setup
    magtag.peripherals.neopixel_disable = False
    magtag.peripherals.neopixels.fill((100, 0, 100))
    # Loop
    response = requests.get(
        secrets["endpoint"] + "/api/stock",
        headers={"GROCRY-API-KEY": secrets["api_key"]},
    )
    raise Exception(response.text)
    time.sleep(0.01)
