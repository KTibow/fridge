import time
from adafruit_magtag.magtag import MagTag
magtag = MagTag()
magtag.peripherals.neopixels.fill((255, 50, 0))
while True:
  time.sleep(0.01)
