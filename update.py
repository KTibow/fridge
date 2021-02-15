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
neopixels_enabled.value = False # It is false, but it's also LOW.
import neopixel
builtin_neopixels = neopixel.NeoPixel(board.NEOPIXEL, 4)
external_neopixels = neopixel.NeoPixel(board.A1, 30)
builtin_neopixels.fill((0, 255, 255))
external_neopixels.fill((128, 0, 255))
# Wait
import time
time.sleep(5)
