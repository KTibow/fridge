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

mt = MagTag(rotation=180)
wakeup_cause = alarm.wake_alarm
if wakeup_cause is None:
    print("Initial boot!")
    mt.set_background("booting.bmp")
    mt.add_text(
        text_font="segoe-ui-12.pcf",
        text_anchor_point=(0.5, 0),
        text_position=(64, 148),
    )
    mt.set_text("< WiFi >")

mt.network.connect()

if wakeup_cause is None:
    mt.set_text("< Data >")

# mt.exit_and_deep_sleep(1)