# Imports
import time
import terminalio
from secrets import secrets

old_time = ""
unix_time = 1610000000
overdue = ""
leftovers = ""


def update_time():
    # Time
    global current_time
    global unix_time
    old_time = current_time
    response = requests.get("http://worldtimeapi.org/api/ip").json()
    unix_time = response["unixtime"] + response["raw_offset"]
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
    current_time = time.localtime(unix_time)
    current_time = f"{current_time.tm_hour % 12}:{current_time.tm_min:02}"
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
        if magtag.peripherals.any_button_pressed:
            magtag.peripherals.neopixels.fill((0, 100, 100))
            time.sleep(1)
            break
        if time.monotonic() - last_update > 15:
            magtag.peripherals.neopixel_disable = False
            magtag.peripherals.neopixels.fill((30, 0, 30))
            try:
                update()
            except Exception:
                pass
            last_update = time.monotonic()
            magtag.peripherals.neopixels.fill((0, 0, 0))
            magtag.peripherals.neopixel_disable = True
        draw()
        time.sleep(0.2)
        unix_time += 0.2
