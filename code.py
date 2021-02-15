# Credit to icons8 for icons
# Imports
from adafruit_magtag.magtag import MagTag  # Control the MagTag
import time  # Wait for stuff and current time

# Display-related imports
import board  # Refresh display

# API-related imports
from secrets import secrets  # API keys
import rtc  # Update the current time

# Functions
def update_time():
    global the_time
    global the_date
    try:
        response = magtag.network.fetch("http://worldtimeapi.org/api/ip").json()
    except Exception as e:
        print("Exception while fetching time:", e)
    else:
        rtc.RTC().datetime = time.localtime(
            response["unixtime"] + response["raw_offset"]
        )


def update_grocy(step=0, data=None, recursion=0):
    global overdue_food
    global ready_to_eat_food
    if recursion > 5:
        return
    if step == 0:  # Get userfields
        try:
            response = magtag.network.fetch(
                secrets["endpoint"] + "/api/objects/products",
                headers={
                    "GROCY-API-KEY": secrets["api_key"],
                    "accept": "application/json",
                },
            ).json()
        except Exception as e:
            print("Exception while fetching food:", e)
            print("Trying again.")
            update_grocy(recursion=recursion + 1)
        else:
            data = []
            for food in response:
                if food["userfields"]:
                    data.append(food["name"])
            step = 1
    if step == 1:  # Get what's in stock
        try:
            response = magtag.network.fetch(
                secrets["endpoint"] + "/api/stock",
                headers={
                    "GROCY-API-KEY": secrets["api_key"],
                    "accept": "application/json",
                },
            ).json()
        except Exception as e:
            print("Exception while fetching food:", e)
            print("Trying again.")
            update_grocy(step=1, data=data, recursion=recursion + 1)
        else:
            ready_to_eat_food = []
            overdue_food = []
            for food in response:
                if food["product"]["name"] in data and float(food["amount"]) > 0:
                    ready_to_eat_food.append(food["product"]["name"])
                food_date = food["best_before_date"].split("-")
                if (
                    time.localtime().tm_year > int(food_date[0])
                    or (
                        time.localtime().tm_year == int(food_date[0])
                        and time.localtime().tm_mon > int(food_date[1])
                    )
                    or (
                        time.localtime().tm_year == int(food_date[0])
                        and time.localtime().tm_mon == int(food_date[1])
                        and time.localtime().tm_mday > int(food_date[2])
                    )
                ):
                    overdue_food.append(food["product"]["name"])


def draw():
    global last_render_state
    current_time = time.localtime()
    hours = current_time.tm_hour
    if hours == 0:
        hours = 12
    elif hours > 12 and hours < 24:
        hours = hours - 12
    time_status = f"{hours}:{current_time.tm_min:02}"
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
magtag.peripherals.neopixels[2] = (0, 255, 150)
try:
    magtag.network.connect()
except Exception as e:
    time.sleep(board.DISPLAY.time_to_refresh)
    magtag.graphics.set_background("wifi_error.bmp")
    board.DISPLAY.refresh()
    raise e
magtag.peripherals.neopixels[3] = (0, 255, 0)
magtag.peripherals.neopixels[2] = (0, 255, 50)
# Global stuff
# General
last_render_state = [None, None, None]
# Time
time_update_interval = 120
last_time_update = time_update_interval * -1  # Trigger time update on first run
# Grocy
overdue_food = []
ready_to_eat_food = []
grocy_update_interval = 300
last_grocy_update = grocy_update_interval * -1  # Trigger grocy update on first run

# Initial time pull
magtag.peripherals.neopixels[1] = (0, 150, 200)
try:
    update_time()
except Exception as e:
    time.sleep(board.DISPLAY.time_to_refresh)
    magtag.graphics.set_background("api_error.bmp")
    board.DISPLAY.refresh()
    raise e
magtag.peripherals.neopixels[1] = (0, 150, 150)

# Initial grocy pull
magtag.peripherals.neopixels[0] = (0, 100, 250)
try:
    update_grocy()
except Exception as e:
    time.sleep(board.DISPLAY.time_to_refresh)
    magtag.graphics.set_background("api_error.bmp")
    board.DISPLAY.refresh()
    raise e
magtag.peripherals.neopixels[0] = (0, 100, 200)

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
    if magtag.peripherals.battery < 3.5:
        break
    time.sleep(0.1)
