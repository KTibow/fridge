# Imports
import time
import terminalio
from secrets import secrets


def main():
    # Setup
    magtag.peripherals.neopixel_disable = False
    magtag.peripherals.neopixels.fill((100, 0, 100))
    time = ""
    weather = ""
    overdue = ""
    leftovers = ""
    magtag.add_text(
        text_font=terminalio.FONT,
        text_position=(
            50,
            (magtag.graphics.display.height // 2) - 1,
        ),
        text_scale=1,
    )
    magtag.set_text("It's 4:03 PM.")
    # Loop
    while True:
        if magtag.peripherals.any_button_pressed:
            magtag.peripherals.neopixels.fill((0, 100, 100))
            time.sleep(1)
            break
        response = requests.get(
            secrets["endpoint"] + "/api/stock",
            headers={
                "GROCY-API-KEY": secrets["api_key"],
                "accept": "application/json",
            },
        )
        print(response.json())
        time.sleep(0.01)
