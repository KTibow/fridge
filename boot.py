# Credit to icons8 for icons.
# Imports
from adafruit_magtag.magtag import MagTag  # Control the MagTag

# Should update question imports
import time  # Wait for stuff
import board  # Refresh display

countdown_enabled = False
try:
    from animations import countdown, sin_animate  # Various animations

    countdown_enabled = True
except Exception:
    pass

# OTA-related imports
import storage  # Mount the code
import microcontroller  # Reset once it's downloaded

# Ask user if they want to go
magtag = MagTag()
magtag.peripherals.neopixel_disable = False
magtag.peripherals.neopixels.fill((0, 50, 50))  # Loading LED
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


if (
    countdown_enabled and countdown(0, 50, 50, 3, magtag, send_response)
) or not countdown_enabled:
    should_update = True


magtag.peripherals.neopixels.fill((0, 0, 0))

# Update
if should_update:
    time.sleep(board.DISPLAY.time_to_refresh)
    magtag.graphics.set_background("installing.bmp")
    board.DISPLAY.refresh()
    magtag.peripherals.neopixels[3] = (125, 25, 255)  # Added brightness - in progress
    magtag.peripherals.neopixels[2] = (130, 60, 255)  # Added brightness - in progress
    # I added some extra red (105-130)
    # And removed some green (75-60) because it looked too white
    # Set up WiFi
    try:
        magtag.network.connect()
    except Exception as e:
        time.sleep(board.DISPLAY.time_to_refresh)
        magtag.graphics.set_background("wifi_error.bmp")
        board.DISPLAY.refresh()
        while board.DISPLAY.busy:
            pass
        raise e
    magtag.peripherals.neopixels[3] = (100, 0, 255)  # Normal brightness - done
    magtag.peripherals.neopixels[2] = (80, 50, 255)  # Normal brightness - done
    # Download code
    magtag.peripherals.neopixels[1] = (60, 130, 255)  # Added brightness - in progress
    # I added some extra blue (105-130)
    # And removed some green (75-60) because it looked too white
    all_files = []
    for file_name in ["animations.py", "code.py"]:
        try:
            all_files.append(
                [
                    file_name,
                    magtag.network.fetch(
                        f"https://raw.githubusercontent.com/KTibow/fridge/main/{file_name}"
                    ).text,
                ]
            )
        except Exception as e:
            print(e)
            magtag.set_text("Download error " + str(e))
            raise e
    magtag.peripherals.neopixels[1] = (50, 80, 255)  # Normal brightness - done
    # Change code
    magtag.peripherals.neopixels[0] = (25, 125, 255)  # Added brightness - in progress
    try:
        storage.remount("/", False)
        for file_name, file_content in all_files:
            with open(f"/{file_name}", "w") as code_file:
                code_file.write(file_content)
                code_file.flush()
    except Exception as e:
        print(e)
        magtag.set_text("Changing code error " + str(e))
        raise e
    finally:
        storage.remount("/", True)
    magtag.peripherals.neopixels[0] = (0, 100, 255)  # Normal brightness - done
    # Tell user that it's done
    time.sleep(board.DISPLAY.time_to_refresh)
    magtag.graphics.set_background("updates_complete.bmp")
    board.DISPLAY.refresh()
    while board.DISPLAY.busy:
        if countdown_enabled:
            sin_animate(100, 0, 255, 0, 4, magtag)
    start_time = time.monotonic()
    while time.monotonic() - start_time < 2:
        if countdown_enabled:
            sin_animate(100, 0, 255, 0, 4, magtag)
    magtag.peripherals.neopixels.fill((0, 0, 0))
    microcontroller.reset()

magtag.peripherals.neopixel_disable = True
