# Display updating image
import displayio
import board

epd = board.DISPLAY
with open("/updating.bmp", "rb") as bitmap_file:
    bitmap = displayio.OnDiskBitmap(bitmap_file)
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())
    group = displayio.Group()
    group.append(tile_grid)
    epd.show(group)
    epd.refresh()

# Initial neopixel config
import digitalio

neopixels_enabled = digitalio.DigitalInOut(board.NEOPIXEL_POWER)
neopixels_enabled.switch_to_output()
neopixels_enabled.value = False  # It is false, but it's also LOW.
import neopixel

builtin_neopixels = neopixel.NeoPixel(board.NEOPIXEL, 4, auto_write=False)
external_neopixels = neopixel.NeoPixel(board.A1, 30, auto_write=False)

# Pattern
builtin_neopixel_left = 1
builtin_neopixel_right = 2
external_neopixel_left = 19
external_neopixel_right = 19


def update_wifi_render():
    global builtin_neopixel_left
    global builtin_neopixel_right
    builtin_neopixel_left -= 1
    if builtin_neopixel_left < 0:
        builtin_neopixel_left = 1
    builtin_neopixel_right += 1
    if builtin_neopixel_right > 3:
        builtin_neopixel_right = 2
    global external_neopixel_left
    global external_neopixel_right
    external_neopixel_left -= 1
    if external_neopixel_left < 12:
        external_neopixel_left = 19
    external_neopixel_right += 1
    if external_neopixel_right > 26:
        external_neopixel_right = 19


def render_wifi():
    builtin_neopixels.fill((0, 0, 0))
    builtin_neopixels[builtin_neopixel_left] = (0, 255, 255)
    builtin_neopixels[builtin_neopixel_right] = (0, 255, 255)
    external_neopixels.fill((128, 0, 255))
    for i in range(8, 30):
        if i >= external_neopixel_left - 4 and i < external_neopixel_left:
            external_neopixels[i] = (255, 255, 255)
        if i > external_neopixel_right and i <= external_neopixel_right + 4:
            external_neopixels[i] = (255, 255, 255)
    builtin_neopixels.show()
    external_neopixels.show()


# Wait
import time

start_time = time.monotonic()
last_render_update = time.monotonic()
while time.monotonic() - start_time < 2.3:
    if time.monotonic() - last_render_update > 0.1:
        update_wifi_render()
        last_render_update = time.monotonic()
    render_wifi()

# Actually connect
import wifi
from secrets import secrets

tries = 0
error = ""
while tries < 3:
    try:
        wifi.radio.connect(secrets["ssid"], secrets["password"])
    except Exception as e:
        tries += 1
        error = e
    else:
        break
if tries == 3:
    time.sleep(epd.time_to_refresh)
    with open("/wifi_error.bmp", "rb") as bitmap_file:
        bitmap = displayio.OnDiskBitmap(bitmap_file)
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())
        group = displayio.Group()
        group.append(tile_grid)
        epd.show(group)
        epd.refresh()
