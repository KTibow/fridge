# Imports
import time
import terminalio
from secrets import secrets


current_time = ""
weather = ""
overdue = ""
leftovers = ""

def update():
    global current_time
    response = requests.get(
        "http://worldtimeapi.org/api/ip"
    ).json()
    current_time = response["unixtime"] + response["raw_offset"]
    current_time = time.localtime(current_time)
    current_time = f"{current_time.tm_hour % 12}:{current_time.tm_min}"
    response = requests.get(
        secrets["endpoint"] + "/api/stock",
        headers={
            "GROCY-API-KEY": secrets["api_key"],
            "accept": "application/json",
        },
    )
    print(response.json())


def main():
    # Setup
    magtag.peripherals.neopixel_disable = False
    magtag.peripherals.neopixels.fill((100, 0, 100))
    magtag.add_text(
        text_font=terminalio.FONT,
        text_position=(
            50,
            (magtag.graphics.display.height // 2) - 1,
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
        if time.monotonic() - last_update > 20:
            update()
            magtag.set_text(current_time)
            last_update = time.monotonic()
        time.sleep(1)
