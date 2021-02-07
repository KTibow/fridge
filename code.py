# Imports
import time
from secrets import secrets
def main():
    # Setup
    magtag.peripherals.neopixel_disable = False
    magtag.peripherals.neopixels.fill((100, 0, 100))
    # Loop
    while True:
      response = requests.get(secrets["endpoint"] + "/api/stock")
      raise Exception(response.text)
      time.sleep(0.01)
