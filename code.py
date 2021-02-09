# Imports
from adafruit_magtag.magtag import MagTag  # Control the MagTag
import time  # Wait for stuff

# API-related imports
from secrets import secrets  # WiFi passwords
import wifi  # Connect to WiFi
import socketpool  # Set up a pool of sockets
import ssl  # Securely connect to APIs
import adafruit_requests  # Actually talk to APIs

# Functions
def update_time():
    global the_time
    try:
        response = requests.get("http://worldtimeapi.org/api/ip").json()
    except Exception as e:
        print("Exception while fetching time:", e)
    else:
        the_time = response["datetime"].split("T")[1].split(":")
        the_time[2] = the_time[2].split("-")[0]
        the_time = [int(the_time[0]), int(the_time[1]), float(the_time[2])]


def update_grocy():
    global the_time


def draw():
    global last_render_state
    hours = the_time[0]
    if hours == 0:
        hours = 12
    elif hours > 12 and hours < 24:
        hours = hours - 12
    status = f"{hours}:{the_time[1]:02}"
    if last_render_state != status:
        magtag.set_text(status, 2)
    last_render_state = status


# Initialize
magtag = MagTag()
magtag.add_text(
    text_font="Open Sans-26-r.pcf",
    text_position=(
        5,
        20,
    ),
    text_scale=1,
)
magtag.peripherals.neopixel_disable = False
magtag.peripherals.neopixels.fill((0, 0, 0))

# Connect to WiFi
magtag.add_text(
    text_font="Open Sans-10-r.pcf",
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
the_time = [3, 14, 15.9]
last_time_bump = time.monotonic()
time_update_interval = 500
last_time_update = time_update_interval * -1  # Trigger time update on first run
grocy_update_interval = 500
last_grocy_update = (
    grocy_update_interval * -1
)  # Trigger grocy update on first run

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
time.sleep(1)
magtag.peripherals.neopixels.fill((0, 0, 0))
magtag.peripherals.neopixel_disable = True
magtag.set_text("", 1)
magtag.set_text("", 0)
magtag.add_text(
    text_font="Open Sans-26-r.pcf",
    text_position=(
        10,
        30,
    ),
    text_scale=2,
)
while True:
    # Make API calls
    if time.monotonic() - last_time_update > time_update_interval:
        update_time()
        last_time_update = time.monotonic()
    draw()
    if time.monotonic() - last_time_bump > 0.25:  # Update time
        the_time[2] += 0.25
        if the_time[2] == 60:
            the_time[1] += 1
            the_time[2] -= 60
            if the_time[1] == 60:
                the_time[0] += 1
                the_time[1] -= 60
        last_time_bump = time.monotonic()
    time.sleep(0.01)
