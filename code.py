# Credit to icons8 for icons
# Imports
from adafruit_magtag.magtag import MagTag  # Control the MagTag
import time  # Wait for stuff

# Display-related imports
import board  # Refresh display

# API-related imports
from secrets import secrets  # WiFi passwords
import wifi  # Connect to WiFi
import socketpool  # Set up a pool of sockets
import ssl  # Securely connect to APIs
import adafruit_requests  # Actually talk to APIs

# Functions
def update_time():
    global the_time
    global the_date
    try:
        response = requests.get("http://worldtimeapi.org/api/ip").json()
    except Exception as e:
        print("Exception while fetching time:", e)
    else:
        the_date = response["datetime"].split("T")[0].split("-")
        the_date = [int(date_item) for date_item in the_date]
        the_time = response["datetime"].split("T")[1].split(":")
        the_time[2] = the_time[2].split("-")[0]
        the_time = [int(the_time[0]), int(the_time[1]), float(the_time[2])]


def update_grocy():
    global overdue_food
    global ready_to_eat_food
    food_to_count_as_ready = []
    try:
        response = requests.get(
            secrets["endpoint"] + "/api/objects/products",
            headers={
                "GROCY-API-KEY": secrets["api_key"],
                "accept": "application/json",
            },
        ).json()
    except Exception as e:
        print("Exception while fetching food:", e)
    else:
        for food in response:
            if food["userfields"]:
                food_to_count_as_ready.append(food["name"])
    try:
        response = requests.get(
            secrets["endpoint"] + "/api/stock",
            headers={
                "GROCY-API-KEY": secrets["api_key"],
                "accept": "application/json",
            },
        ).json()
    except Exception as e:
        print("Exception while fetching food:", e)
    else:
        ready_to_eat_food_temp = []
        for food in response:
            if food["product"]["name"] in food_to_count_as_ready and int(food["amount"]) > 0:
                ready_to_eat_food_temp.append(food["product"]["name"])
        ready_to_eat_food = ready_to_eat_food_temp.copy()
    try:
        response = requests.get(
            secrets["endpoint"] + "/api/stock/volatile",
            headers={
                "GROCY-API-KEY": secrets["api_key"],
                "accept": "application/json",
            },
        ).json()
    except Exception as e:
        print("Exception while fetching food:", e)
    else:
        overdue_food_temp = []
        for food in response["overdue_products"]:
            overdue_food_temp.append(food["product"]["name"])
        overdue_food = overdue_food_temp.copy()


def draw():
    global last_render_state
    hours = the_time[0]
    if hours == 0:
        hours = 12
    elif hours > 12 and hours < 24:
        hours = hours - 12
    time_status = f"{hours}:{the_time[1]:02}"
    old_food_status = ", ".join(overdue_food)
    ready_food_status = ", ".join(ready_to_eat_food)
    if not overdue_food:
        old_food_status = f"Nothing is overdue."
    if not ready_to_eat_food:
        ready_food_status = f"Nothing is ready to eat."
    if last_render_state[0] != time_status:
        magtag.set_text(time_status)
    if last_render_state[1] != old_food_status:
        magtag.set_text(old_food_status, 1)
    if last_render_state[2] != ready_food_status:
        magtag.set_text(ready_food_status, 2)
    last_render_state = [time_status, old_food_status, ready_food_status]


# Initialize
magtag = MagTag()
magtag.peripherals.neopixel_disable = False
magtag.peripherals.neopixels.fill((0, 0, 0))

# Connect to WiFi
time.sleep(board.DISPLAY.time_to_refresh)
magtag.graphics.set_background("connecting.bmp")
board.DISPLAY.refresh()
magtag.peripherals.neopixels[3] = (0, 255, 100)
try:
    wifi.radio.connect(secrets["ssid"], secrets["password"])
except Exception as e:
    time.sleep(board.DISPLAY.time_to_refresh)
    magtag.graphics.set_background("wifi_error.bmp")
    board.DISPLAY.refresh()
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
# General
last_render_state = [None, None, None]
# Time
the_time = [3, 14, 15.9]
last_time_bump = time.monotonic()
time_update_interval = 120
last_time_update = time_update_interval * -1  # Trigger time update on first run
# Grocy
the_date = [2021, 2, 10]
overdue_food = []
ready_to_eat_food = []
grocy_update_interval = 300
last_grocy_update = grocy_update_interval * -1  # Trigger grocy update on first run

# Initial time pull
magtag.peripherals.neopixels[1] = (0, 255, 100)
try:
    update_time()
except Exception as e:
    time.sleep(board.DISPLAY.time_to_refresh)
    magtag.graphics.set_background("api_error.bmp")
    board.DISPLAY.refresh()
    raise e
magtag.peripherals.neopixels[1] = (0, 255, 0)

# Initial grocy pull
magtag.peripherals.neopixels[0] = (0, 255, 100)
try:
    update_grocy()
except Exception as e:
    time.sleep(board.DISPLAY.time_to_refresh)
    magtag.graphics.set_background("api_error.bmp")
    board.DISPLAY.refresh()
    raise e
magtag.peripherals.neopixels[0] = (0, 255, 0)

# Event loop
time.sleep(1)
magtag.peripherals.neopixels.fill((0, 0, 0))
magtag.peripherals.neopixel_disable = True
magtag.graphics.set_background("main_ui.bmp")
magtag.add_text(
    text_font="Open Sans-26-r.pcf",
    text_position=(
        2,
        2,
    ),
    text_scale=2,
    text_anchor_point=(0, 0),
)
magtag.add_text(
    text_font="Open Sans-10-r.pcf",
    text_position=(
        210,
        5,
    ),
    text_scale=1,
    text_wrap=15,
    line_spacing=0.75,
    text_anchor_point=(0, 0),
)
magtag.add_text(
    text_font="Open Sans-10-r.pcf",
    text_position=(
        40,
        70,
    ),
    text_scale=1,
    text_wrap=40,
    line_spacing=0.75,
)
# Update last bump
last_time_bump = time.monotonic()
while True:
    # Make API calls
    if time.monotonic() - last_time_update >= time_update_interval:
        update_time()
        last_time_update = time.monotonic()
    if time.monotonic() - last_grocy_update >= grocy_update_interval:
        update_grocy()
        last_grocy_update = time.monotonic()
    if (
        not magtag.peripherals.button_a_pressed
        and magtag.peripherals.button_b_pressed
        and not magtag.peripherals.button_c_pressed
        and magtag.peripherals.button_d_pressed
    ):
        magtag.peripherals.neopixel_disable = False
        magtag.peripherals.neopixels.fill((255, 255, 255))
        while magtag.peripherals.any_button_pressed:
            pass
        magtag.peripherals.neopixels.fill((0, 0, 0))
        magtag.peripherals.neopixel_disable = True
    draw()
    if time.monotonic() - last_time_bump >= 0.5:  # Update time
        print("Time from", the_time)
        the_time[2] += 0.5
        last_time_bump += 0.5
        if the_time[2] >= 60:
            the_time[1] += 1
            the_time[2] -= 60
            if the_time[1] >= 60:
                the_time[0] += 1
                the_time[1] -= 60
        print("To", the_time)
    if magtag.peripherals.battery < 3.3:
        break
    time.sleep(0.1)
