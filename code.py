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

from adafruit_magtag.magtag import MagTag  # Main MagTag
import alarm  # Deep sleep
import neopixel, board  # External NeoPixel strip
import time  # Wait and get time

mt = MagTag(rotation=180)
light_strip = neopixel.NeoPixel(board.A1, 30)
light_strip.fill((255, 255, 0))

def display_error(e):
    light_strip.fill((0, 0, 0))
    for i in range(30):
        if i % 7 == 0:
            light_strip[i] = (255, 0, 0)
    mt.add_text(
        text_font="segoe-ui-12.pcf",
        text_anchor_point=(0, 0),
        text_position=(10, 254),
    )
    if alarm.wake_alarm is None:
        mt.set_text("Error!", 1, auto_refresh=False)
    else:
        mt.set_text("Error!", auto_refresh=False)
    mt.graphics.qrcode(str.encode(str(e)), qr_size=2, x=60, y=240)
    time.sleep(mt.display.time_to_refresh)
    mt.display.refresh()
    mt.exit_and_deep_sleep(60)

if alarm.wake_alarm is None:
    print("Initial boot!")
    mt.set_background("booting.bmp")
    mt.add_text(
        text_font="segoe-ui-12.pcf",
        text_anchor_point=(0.5, 0),
        text_position=(64, 148),
    )
    mt.set_text("WiFi")

tries = 0
while tries < 3:
    try:
        mt.network.connect()
    except Exception as e:
        if tries < 3:
            print("Error connecting to WiFi. Trying again.")
            tries += 1
        else:
            display_error(e)
    else:
        break

if alarm.wake_alarm is None:
    mt.set_text("Data")

try:
    data = mt.network.fetch(mt.network._secrets["endpoint"] + f"{mt.peripherals.battery}/").json()
except Exception as e:
    display_error(e)

mt.add_text(
    text_font="segoe-ui-12.pcf",
    text_anchor_point=(0, 0),
    text_position=(5, 5),
    line_spacing=0.88,
)
the_output = ""

if len(data["ready_to_eat"]) > 0:
    the_output += "\nReady to eat:\n\n"
    for item in data["ready_to_eat"]:
        the_output += f"  - {item}\n"
if len(data["missing"]) > 0:
    the_output += "\nBuy more of:\n\n"
    for item in data["missing"]:
        the_output += f"  - {item}\n"
if len(data["overdue"]) > 0:
    the_output += "\nOverdue:\n\n"
    for item in data["overdue"]:
        the_output += f"  - {item}\n"

the_output = the_output.strip()
if alarm.wake_alarm is None:
    mt.set_text("", auto_refresh=False)
    mt.graphics.set_background(0xFFFFFF)
    mt.set_text(the_output, 1)
else:
    mt.set_text(the_output)

light_strip.fill((0, 0, 0))
mt.exit_and_deep_sleep(60 * 60)
