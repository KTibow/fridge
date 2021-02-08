# Imports
from adafruit_magtag.magtag import MagTag  # Control the MagTag
import terminalio # Get font
import time # Wait for stuff
# API-related imports
from secrets import secrets # WiFi passwords
import wifi # Connect to WiFi
import socketpool # Set up a pool of sockets
import ssl # Securely connect to APIs
import adafruit_requests # Actually talk to APIs

# Global stuff
current_time = ""

# Functions
def update_time():
    global current_time

# Initialize
magtag = MagTag()
magtag.add_text(
    text_font=terminalio.FONT,
    text_position=(
        10,
        10,
    ),
    text_scale=3,
)
magtag.peripherals.neopixel_disable = False
magtag.peripherals.neopixels.fill((0, 0, 0))

# Connect to WiFi
magtag.set_text("Connecting...")
magtag.add_text(
    text_font=terminalio.FONT,
    text_position=(
        10,
        50,
    ),
    text_scale=1,
)
magtag.set_text("1: WiFi, 2: Sockets, 3: Time, 4: Grocy", 1)
magtag.peripherals.neopixels[3] = (0, 255, 100)
try:
    wifi.radio.connect(secrets["ssid"], secrets["password"])
except Exception as e:
    magtag.set_text("WiFi error.")
    raise e
magtag.peripherals.neopixels[3] = (0, 255, 0)
# Sockets
magtag.peripherals.neopixels[2] = (0, 255, 100)
try:
    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
except Exception as e:
    magtag.set_text("Socket error.")
    raise e
magtag.peripherals.neopixels[2] = (0, 255, 0)

# Event loop
while True:
    time.sleep(0.01)
