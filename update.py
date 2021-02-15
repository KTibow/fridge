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

builtin_neopixels = neopixel.NeoPixel(board.NEOPIXEL, 4)
external_neopixels = neopixel.NeoPixel(board.A1, 30)
# Pattern
builtin_neopixel_left = 1
builtin_neopixel_right = 2
external_neopixel_left = 10
external_neopixel_right = 11


def render_wifi():
    builtin_neopixels.fill((0, 255, 255))
    builtin_neopixels[builtin_neopixel_left] = (255, 255, 255)
    builtin_neopixels[builtin_neopixel_right] = (255, 255, 255)
    external_neopixels.fill((128, 0, 255))
    for i in range(8, 30):
        if i > external_neopixel_left - 4 and i < external_neopixel_left:
            external_neopixels[i] = (255, 255, 255)
        if i > external_neopixel_right and i < external_neopixel_right + 4:
            external_neopixels[i] = (255, 255, 255)


# Wait
import time

start_time = time.monotonic()
while time.monotonic() - start_time < 5:
    render_wifi()
