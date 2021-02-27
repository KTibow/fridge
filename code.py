try:
    import os, microcontroller
    os.stat("/latest_boot.py")
    with open("/boot.py", "w") as boot:
        with open("/latest_boot.py", "r") as new_boot:
            print("Updating...")
            boot.write(new_boot.read())
            boot.flush()
    os.remove("/latest_boot.py")
    microcontroller.reset()
except Exception:
    pass

from adafruit_magtag.magtag import MagTag # Main MagTag
import alarm # Deep sleep
import neopixel, board # External NeoPixel strip
import time # Wait and get time

mt = MagTag(rotation=180)
wakeup_cause = alarm.wake_alarm
light_strip = neopixel.NeoPixel(board.A1, 30)
if wakeup_cause is None:
    print("Initial boot!")
    mt.set_background("booting.bmp")
    mt.add_text(
        text_font="segoe-ui-12.pcf",
        text_anchor_point=(0.5, 0),
        text_position=(64, 148),
    )
    mt.set_text("WiFi")

tries = 5
error = ""
while tries > 0:
    try:
        mt.network.connect()
    except Exception as e:
        error = str(e)
    else:
        break
    tries -= 1

if tries == 0:
    mt.add_text(
        text_font="segoe-ui-12.pcf",
        text_anchor_point=(0, 0),
        text_position=(10, 254),
    )
    if wakeup_cause is None:
        mt.set_text("Error!", 1, auto_refresh=False)
    else:
        mt.set_text("Error!", auto_refresh=False)
    mt.graphics.qrcode(str.encode(error), qr_size=2, x=60, y=240)
    mt.display.refresh()
    mt.peripherals.play_tone(1000, 0.5)
    mt.exit_and_deep_sleep(60)

if wakeup_cause is None:
    mt.set_text("Data")

data = mt.network.fetch("http://192.168.1.3:5338/").json()
mt.add_text(
    text_font="segoe-ui-12.pcf",
    text_anchor_point=(0, 0),
    text_position=(5, 5),
    line_spacing=0.75,
)

the_output = ""
if len(data["missing"]) > 0:
    the_output += "Buy more of:\n"
    for item in data["missing"]:
        the_output += f"  - {item}\n"
if len(data["overdue"]) > 0:
    the_output += "Overdue:\n"
    for item in data["overdue"]:
        the_output += f"  - {item}\n"
if len(data["ready_to_eat"]) > 0:
    the_output += "Ready to eat:\n"
    for item in data["ready_to_eat"]:
        the_output += f"  - {item}\n"

if wakeup_cause is None:
    mt.set_text("", auto_refresh=False)
    mt.graphics.set_background(0xFFFFFF)
    mt.set_text(the_output, 1)
else:
    mt.set_text(the_output)

mt.exit_and_deep_sleep(60 * 60)
