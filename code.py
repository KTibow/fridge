# Imports
import time
import terminalio
from secrets import secrets

old_time = ""
now_time = ""
overdue = ""
leftovers = ""


def update_time():
    # Time
    global now_time
    response = requests.get("http://worldtimeapi.org/api/ip").json()
    now_time = response["datetime"].split("T")[1].split(":")[0:2]


def update_food():
    # Food
    response = requests.get(
        secrets["endpoint"] + "/api/stock",
        headers={
            "GROCY-API-KEY": secrets["api_key"],
            "accept": "application/json",
        },
    )
    print(response.json())


def draw():
    # Time
    global old_time
    current_time = [int(time_item) for time_item in now_time]
    print(current_time)
    hours = current_time[0]
    if hours == 0:
        hours = 12
    elif hours > 12 and hours < 24:
        hours = hours - 12
    current_time = f"{hours}:{current_time[1]:02}"
    if old_time != current_time:
        magtag.set_text(current_time)
    old_time = current_time


def main():
    # Setup
    global unix_time
    magtag.peripherals.neopixels.fill((0, 0, 0))
    magtag.peripherals.neopixel_disable = True
    # Previously: (magtag.graphics.display.height // 2) - 1
    magtag.add_text(
        text_font=terminalio.FONT,
        text_position=(
            10,
            10,
        ),
        text_scale=3,
    )
    # Loop
    last_update = time.monotonic()
    while True:
        # Exit
        if magtag.peripherals.any_button_pressed:
            magtag.peripherals.neopixels.fill((0, 100, 100))
            time.sleep(1)
            break
        # Update data
        if time.monotonic() - last_update > 15:
            try:
                update_time()
                update_food()
            except Exception as e:
                print("Updating exception:", e)
            last_update = time.monotonic()
        # Draw
        try:
            draw()
        except Exception as e:
            print("error drawing", e)
        time.sleep(0.2)
