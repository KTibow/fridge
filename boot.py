# Initial message
from adafruit_magtag.magtag import MagTag
import terminalio
magtag = MagTag()
magtag.add_text(
    text_font=terminalio.FONT,
    text_position=(
        50,
        (magtag.graphics.display.height // 2) - 1,
    ),
    text_scale=3,
)
magtag.set_text("Loading")
# Everything else
import time
import storage
# Wifi related
import adafruit_requests
import wifi
import ssl
import socketpool
from secrets import secrets

magtag.peripherals.neopixel_disable = False
storage.remount("/", False)

try:
    magtag.set_text("Connecting")
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    magtag.set_text("Updating")
    # Init
    magtag.peripherals.neopixels.fill((255, 0, 0))
    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    # Download
    magtag.peripherals.neopixels.fill((255, 255, 0))
    response = requests.get("https://raw.githubusercontent.com/KTibow/fridge/main/code.py")
    with open("/code.py", "w") as test:
        # Write
        magtag.peripherals.neopixels.fill((0, 255, 0))
        test.write(response.text)
        test.flush()
finally:
    storage.remount("/", True)
    magtag.peripherals.neopixel_disable = True
