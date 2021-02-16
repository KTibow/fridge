import board  # Pins and display
import displayio  # Display
import digitalio  # Enable neopixels

epd = board.DISPLAY


def display_image(filename):
    with open(f"/{filename}.bmp", "rb") as bitmap_file:
        bitmap = displayio.OnDiskBitmap(bitmap_file)
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())
        group = displayio.Group()
        group.append(tile_grid)
        epd.show(group)
        epd.refresh()

def change_builtin_neopixel_status(is_enabled)
