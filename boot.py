# Credit to icons8 for icons.
# Imports
from adafruit_magtag.magtag import MagTag  # Control the MagTag

# Should update question imports
import time  # Wait for stuff
import board  # Refresh display
import animations # Countdown

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
def send_response():
    if magtag.peripherals.any_button_pressed:
        return True
if countdown(0, 255, 50, 4, magtag, send_response):
    should_update = True
    

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
        main_code_text = requests.get(
            "https://raw.githubusercontent.com/KTibow/fridge/main/code.py"
        ).text
    except Exception as e:
        print(e)
        magtag.set_text("Download error " + str(e))
        raise e
    try:
        animations_code_text = requests.get(
            "https://raw.githubusercontent.com/KTibow/fridge/main/animations.py"
        ).text
    except Exception as e:
        print(e)
        magtag.set_text("Download error " + str(e))
        raise e
    # Change code
    magtag.peripherals.neopixels[0] = (0, 255, 0)
    try:
        storage.remount("/", False)
        with open("/code.py", "w") as the_code:
            the_code.write(main_code_text)
            the_code.flush()
        with open("/animations.py", "w") as the_code:
            the_code.write(animations_code_text)
            the_code.flush()
    except Exception as e:
        print(e)
        magtag.set_text("Changing code error " + str(e))
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
