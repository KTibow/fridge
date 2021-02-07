# Imports
import time
import terminalio
from secrets import secrets


def update():
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
    current_time = ""
    weather = ""
    overdue = ""
    leftovers = ""
    magtag.add_text(
        text_font=terminalio.FONT,
        text_position=(
            50,
            (magtag.graphics.display.height // 2) - 1,
        ),
        text_scale=3,
    )
    magtag.set_text("It's 4:03 PM.")
    # Loop
    last_update = time.monotonic()
    while True:
        if magtag.peripherals.any_button_pressed:
            magtag.peripherals.neopixels.fill((0, 100, 100))
            time.sleep(1)
            break
        if time.monotonic() - last_update > 15:
            update()
            last_update = time.monotonic()
        time.sleep(1)
