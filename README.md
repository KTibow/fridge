![Leftunder logo](/leftunder-color.svg)
# The Leftunder Project
Hosting, docs, and more for the Leftunder Project.
## What is it?
The Leftunder Project is basically just some code for the Adafruit MagTag. Except it has lots of cool stuff:
- OTA
- An online serial console
- Logo + deep sleep

### What's the Adafruit MagTag?
It's a thing to go on your fridge with 4 buttons, 4 NeoPixels, a e-ink display, a battery port, and some addon-ports.
## How can I use the accessories?
My code is built to work with a 30 pixel LED strip plugged into A1. It's on the bottom of the freezer, and I utilize about position 8 to the end.
### For OTA:
You may need to change some stuff for boards that aren't the Adafruit MagTag.
- Make sure you have all of the libraries required.
- Copy over `boot.py`, `ota.bmp`, `black-ops-one-40.pcf`, and `segoe-ui-12.pcf`.
- Add this bit to the top of `code.py`:
```python
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
```
- Post your code to GitHub.
- Change `https://raw.githubusercontent.com/KTibow/fridge/main/{file}` for your username and repo.
- When you're ready to OTA, hold down any of the MagTag's buttons while pressing reset. You can release it once it beeps.

### For serial console:
Make sure you're using an up-to-date version of Chrome or Chrome-based browser (chromium, new edge, etc). Then just visit https://ktibow.github.io/fridge/serial! Hit the connect button, and choose your device. And you can use the terminal like you would use a serial console.
## Attributions
Icons found in the bmp files by Icons8.
