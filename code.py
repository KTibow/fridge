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

# Functions
def update_time():
    global current_time
    response = requests.get("http://worldtimeapi.org/api/ip").json()
    current_time = response["datetime"].split("T")[1].split(":")
    current_time = current_time[0:2] + [current_time[2].split("-")[0]]
    current_time = [float(time_item) for time_item in current_time]

def update_grocy():
    global current_time

def draw():
    magtag.set_text(str(current_time[0:2]))

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
magtag.add_text(
    text_font=terminalio.FONT,
    text_position=(
        10,
        50,
    ),
    text_scale=1,
)
magtag.set_text("Connecting...")
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

# Global stuff
last_render_state = ""
current_time = [3, 14, 15.9]
last_time_bump = time.monotonic()
time_update_interval = 500
time_when_time_updated = time_update_interval * -1 # Trigger time update on first run
grocy_update_interval = 500
time_when_grocy_updated = grocy_update_interval * -1 # Trigger grocy update on first run

# Initial time pull
magtag.peripherals.neopixels[1] = (0, 255, 100)
try:
    update_time()
except Exception as e:
    magtag.set_text("Time API error.")
    raise e
magtag.peripherals.neopixels[1] = (0, 255, 0)

# Initial grocy pull
magtag.peripherals.neopixels[0] = (0, 255, 100)
try:
    update_grocy()
except Exception as e:
    magtag.set_text("Grocy API error.")
    raise e
magtag.peripherals.neopixels[0] = (0, 255, 0)

# Event loop
while True:
    # Make API calls
    if time.monotonic() - time_when_time_updated > time_update_interval:
        update_time()
    draw()
    if time.monotonic() - last_time_bump > 0.25: # Update time
        current_time[2] += 0.25
        if current_time[2] > 60:
            current_time[1] += 1
            current_time[2] -= 60
            if current_time[1] > 60:
                current_time[0] += 1
                current_time[1] -= 60
        last_time_bump = time.monotonic()
    time.sleep(0.01)
