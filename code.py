# Imports
import time
from secrets import secrets


def main():
    # Setup
    magtag.peripherals.neopixel_disable = False
    magtag.peripherals.neopixels.fill((100, 0, 100))
    # Loop
    while True:
        print((
            "GET",
            secrets["endpoint"] + "/api/stock",
            {
                "GROCRY-API-KEY": secrets["api_key"],
                "accept": "application/json",
            },
        ))
        response = requests.request(
            "GET",
            secrets["endpoint"] + "/api/stock",
            headers={
                "GROCRY-API-KEY": secrets["api_key"],
                "accept": "application/json",
            },
        )
        raise Exception(response.text)
        time.sleep(0.01)
