# Check for buttons
from adafruit_magtag.peripherals import Peripherals

mt_p = Peripherals()

if not mt_p.any_button_pressed:
    import sys

    sys.exit()


def deinit(self):
    """Call deinit on all resources to free them"""
    self.neopixels.deinit()
    self._neopixel_disable.deinit()
    self._speaker_enable.deinit()
    for button in self.buttons:
        button.deinit()
    self._batt_monitor.deinit()
    self._light.deinit()


# Immediate feedback via speaker
import board, digitalio, pwmio, time

deinit(mt_p)
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.switch_to_output()
speaker_enable.value = True
speaker = pwmio.PWMOut(board.SPEAKER, variable_frequency=True)

for i in range(300, 700, 100):
    speaker.duty_cycle = 0x8000
    speaker.frequency = i
    time.sleep(0.04)
    speaker.duty_cycle = 0
    time.sleep(0.1)

speaker_enable.deinit()
# Proceed to rendering display
from adafruit_magtag.magtag import MagTag
import neopixel
import math

mt = MagTag(rotation=180, default_bg="ota.bmp")

mt.peripherals.neopixels.fill((32, 0, 255))
mt.add_text(
    text_font="black-ops-one-40.pcf",
    text_anchor_point=(0.5, 0),
    text_position=(64, 14),
)
description_font = "segoe-ui-12.pcf"
mt.add_text(
    text_font=description_font,
    text_anchor_point=(1, 0.5),
    text_position=(87 - 5, 95),
)
mt.add_text(
    text_font=description_font,
    text_anchor_point=(1, 0.5),
    text_position=(87 - 5, 168),
)
mt.add_text(
    text_font=description_font,
    text_anchor_point=(1, 0.5),
    text_position=(87 - 5, 241),
)
mt.set_text("OTA", 0, auto_refresh=False)
mt.set_text("Save", 1, auto_refresh=False)
mt.set_text("Download", 2, auto_refresh=False)
mt.set_text("WiFi", 3, auto_refresh=False)
mt.refresh()

# Show a nice animation when you start
start_anim = time.monotonic()
external_neopixels = neopixel.NeoPixel(board.A1, 30)

mt.peripherals.neopixels.auto_write = False
external_neopixels.auto_write = False

while time.monotonic() - start_anim < 5:
    for i in range(4):
        color = (math.sin(time.monotonic() * 2 + i) + 2) / 3
        mt.peripherals.neopixels[i] = (
            color * 255,
            color * 32,
            0,
        )
    for i in range(30):
        color = (math.sin(time.monotonic() * 2 + i) + 2) / 3
        external_neopixels[i] = (
            color * 255,
            color * 32,
            0,
        )
    mt.peripherals.neopixels.show()
    external_neopixels.show()

# First bit of progress bar
mt.peripherals.neopixels.fill((0, 0, 0))
external_neopixels.fill((0, 0, 0))

mt.peripherals.neopixels[0] = (230, 255, 0)
for i in range(8, 15):
    external_neopixels[i] = (230, 255, 0)

mt.peripherals.neopixels.show()
external_neopixels.show()

# Connect to WiFi
tries = 4
while tries != 0:
    try:
        mt.network.connect()
        break
    except Exception:
        tries -= 1
        mt.peripherals._speaker_enable.value = True
        speaker.duty_cycle = 500
        speaker.frequency = 500
        time.sleep(0.15)
        speaker.frequency = 400
        time.sleep(0.15)
        speaker.duty_cycle = 0
        mt.peripherals._speaker_enable.value = False
if tries == 0:
    mt.peripherals._speaker_enable.value = True
    speaker.duty_cycle = 0x8000
    speaker.frequency = 500
    time.sleep(0.25)
    speaker.frequency = 400
    time.sleep(0.25)
    speaker.duty_cycle = 0
    mt.peripherals._speaker_enable.value = False
    exit()

# Next bit of progress bar
mt.peripherals.neopixels[0] = (25, 255, 0)
for i in range(8, 15):
    external_neopixels[i] = (25, 255, 0)

mt.peripherals.neopixels[1] = (230, 255, 0)
for i in range(15, 22):
    external_neopixels[i] = (230, 255, 0)

mt.peripherals.neopixels.show()
external_neopixels.show()

# Download files
import json

files = {}
for file in ["boot.py", "code.py"]:
    tries = 4
    while tries != 0:
        try:
            files[file] = mt.network.fetch(f"https://raw.githubusercontent.com/KTibow/fridge/main/{file}").text
            break
        except Exception:
            tries -= 1
            mt.peripherals._speaker_enable.value = True
            speaker.duty_cycle = 500
            speaker.frequency = 500
            time.sleep(0.15)
            speaker.frequency = 400
            time.sleep(0.15)
            speaker.duty_cycle = 0
            mt.peripherals._speaker_enable.value = False
    if tries == 0:
        mt.peripherals._speaker_enable.value = True
        speaker.duty_cycle = 0x8000
        speaker.frequency = 500
        time.sleep(0.25)
        speaker.frequency = 400
        time.sleep(0.25)
        speaker.duty_cycle = 0
        mt.peripherals._speaker_enable.value = False

# Final bit of progress bar
mt.peripherals.neopixels[1] = (25, 255, 0)
for i in range(15, 22):
    external_neopixels[i] = (25, 255, 0)

mt.peripherals.neopixels[2] = (230, 255, 0)
for i in range(22, 30):
    external_neopixels[i] = (230, 255, 0)

mt.peripherals.neopixels.show()
external_neopixels.show()

# Save files
import storage
storage.remount("/", False)
for filename, content in files.items():
    if filename != "boot.py":
        with open(filename, "w") as code:
            code.write(content)
            code.flush()
with open("latest_boot.py", "w") as code:
    code.write(files["boot.py"])
    code.flush()

# Finish
mt.peripherals.neopixels[3] = (25, 255, 0)
for i in range(22, 30):
    external_neopixels[i] = (25, 255, 0)
mt.peripherals.neopixels.show()
external_neopixels.show()
