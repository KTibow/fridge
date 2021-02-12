# Credit to icons8 for icons.
# Imports
from adafruit_magtag.magtag import MagTag  # Control the MagTag

# Should update question imports
import time  # Wait for stuff
import board  # Refresh display

# OTA-related imports
from secrets import secrets # WiFi passwords
import wifi # Connect to WiFi
import socketpool # Set up a pool of sockets
import ssl # Securely connect to GitHub for code
import adafruit_requests # Download the code
import storage  # Mount the code
import microcontroller # Reset once it's downloaded

# Ask user if they want to go
magtag = MagTag()
magtag.peripherals.neopixel_disable = False
magtag.peripherals.neopixels.fill((0, 50, 50)) # Loading LED
magtag.graphics.set_background("ota.bmp")
time.sleep(board.DISPLAY.time_to_refresh)
board.DISPLAY.refresh()
while board.DISPLAY.busy:
    pass

# Wait
initial_time = time.monotonic()
should_update = False
while time.monotonic() - initial_time < 4:
    if time.monotonic() - initial_time < 1:
        magtag.peripherals.neopixels.fill((0, 50, 0))
    elif time.monotonic() - initial_time < 2:
        magtag.peripherals.neopixels.fill((50, 50, 0))
    elif time.monotonic() - initial_time < 3:
        magtag.peripherals.neopixels.fill((50, 20, 0))
    else:
        magtag.peripherals.neopixels.fill((50, 0, 0))
    if magtag.peripherals.any_button_pressed:
        should_update = True
        break

magtag.peripherals.neopixels.fill((0, 0, 0))

# Update
if should_update:
    time.sleep(board.DISPLAY.time_to_refresh)
    magtag.graphics.set_background("installing.bmp")
    board.DISPLAY.refresh()
    magtag.peripherals.neopixels[3] = (255, 0, 0)
    # Set up WiFi
    try:
        wifi.radio.connect(secrets["ssid"], secrets["password"])
    except Exception as e:
        time.sleep(board.DISPLAY.time_to_refresh)
        magtag.graphics.set_background("wifi_error.bmp")
        board.DISPLAY.refresh()
        while board.DISPLAY.busy:
            pass
        raise e
    magtag.peripherals.neopixels[2] = (255, 100, 0)
    # Set up sockets
    try:
        pool = socketpool.SocketPool(wifi.radio)
        requests = adafruit_requests.Session(pool, ssl.create_default_context())
    except Exception as e:
        magtag.set_text("Socket error " + e)
        raise e
    # Download code
    magtag.peripherals.neopixels[1] = (255, 255, 0)
    try:
        response = requests.get(
            "https://raw.githubusercontent.com/KTibow/fridge/main/code.py"
        )
    except Exception as e:
        print(e)
        magtag.set_text("Download error " + str(e))
        raise e
    try:
        other_response = requests.get(
            "https://raw.githubusercontent.com/KTibow/fridge/main/animations.py"
        )
    except Exception as e:
        print(e)
        magtag.set_text("Download error " + str(e))
        raise e
    # Change code
    magtag.peripherals.neopixels[0] = (0, 255, 0)
    try:
        storage.remount("/", False)
        with open("/code.py", "w") as the_code:
            the_code.write(response.text)
            the_code.flush()
        with open("/animations.py", "w") as the_code:
            the_code.write(other_response.text)
            the_code.flush()
    except Exception as e:
        magtag.set_text("Changing code error " + e)
        raise e
    finally:
        storage.remount("/", True)
    # Tell user that it's done
    time.sleep(board.DISPLAY.time_to_refresh)
    magtag.graphics.set_background("updates_complete.bmp")
    board.DISPLAY.refresh()
    while board.DISPLAY.busy:
        pass
    magtag.peripherals.neopixels.fill((0, 0, 0))
    time.sleep(2)
    microcontroller.reset()

magtag.peripherals.neopixel_disable = True
