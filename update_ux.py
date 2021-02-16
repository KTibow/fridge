import board  # Pins and display
import time # Wait for display
import displayio  # Display
import digitalio  # Enable neopixels
import neopixel # Use neopixels

epd = board.DISPLAY
neopixels_enabled = digitalio.DigitalInOut(board.NEOPIXEL_POWER)
builtin_neopixels = neopixel.NeoPixel(board.NEOPIXEL, 4, auto_write=False)
external_neopixels = neopixel.NeoPixel(board.A1, 30, auto_write=False)

neopixels_enabled.switch_to_output()

builtin_neopixel_left = 1
builtin_neopixel_right = 2
external_neopixel_left = 19
external_neopixel_right = 19

render_download_offset = 0

def display_image(filename):
    with open(f"/{filename}.bmp", "rb") as bitmap_file:
        bitmap = displayio.OnDiskBitmap(bitmap_file)
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())
        group = displayio.Group()
        group.append(tile_grid)
        epd.show(group)
        time.sleep(epd.time_to_refresh)
        epd.refresh()

def change_builtin_neopixel_status(is_enabled):
    neopixels_enabled.value = not is_enabled # LOW == False == enabled

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

def update_download_render():
    global render_download_offset
    render_download_offset += 1
    render_download_offset %= 4

def render_download():
    builtin_neopixels.fill((0, 0, 0))
    for i in range(4):
        if i % 4 == render_download_offset:
            builtin_neopixels[i] = (0, 255, 255)
    external_neopixels.fill((128, 0, 255))
    for i in range(8, 30):
        if i % 4 == render_download_offset:
            external_neopixels[i] = (255, 255, 255)
    builtin_neopixels.show()
    external_neopixels.show()
