# Imports
import time
import storage
from adafruit_magtag.magtag import MagTag
import sys

# Wifi related
import adafruit_requests
import wifi
import ssl
import socketpool
from secrets import secrets

magtag = MagTag()
magtag.peripherals.neopixel_disable = False
magtag.peripherals.neopixels.fill((255, 75, 0))
# Init wifi
wifi.radio.connect(secrets["ssid"], secrets["password"])
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())
magtag.peripherals.neopixels.fill((50, 0, 255))
# Download
response = requests.get(
    "https://raw.githubusercontent.com/KTibow/fridge/main/code.py"
)

if magtag.peripherals.buttons[0].value:
    try:
        storage.remount("/", False)
        old_code = open("/code.py").read()
        with open("/code.py", "w") as test:
            # Write
            magtag.peripherals.neopixels.fill((0, 255, 0))
            test.write(response.text)
            test.flush()
    except Exception as e:
        print("Exception thrown while updating.")
        print(e)
    storage.remount("/", True)


magtag.peripherals.neopixels.fill((0, 0, 0))
magtag.peripherals.neopixel_disable = True

# Finally code
exec(open("/code.py").read())
main()
