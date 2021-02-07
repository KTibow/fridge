# Imports
import time
from adafruit_magtag.magtag import MagTag
# Wifi related
import adafruit_requests
import wifi
import ssl
import socketpool
from secrets import secrets
# Setup
magtag = MagTag()
magtag.peripherals.neopixel_disable = False
magtag.peripherals.neopixels.fill((100, 50, 0))
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())
magtag.peripherals.neopixels.fill((0, 0, 0))
magtag.peripherals.neopixel_disable = True
# Loop
while True:
  response = requests.get("https://raw.githubusercontent.com/KTibow/fridge/main/code.py")
  raise Exception(response)
  time.sleep(0.01)
