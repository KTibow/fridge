# Show update display and show wifi animation
import update_ux

update_ux.display_image("updating")

import time

start_time = time.monotonic()
last_render_update = time.monotonic()
update_ux.change_builtin_neopixel_status(is_enabled=True)
while time.monotonic() - start_time < 2.3:
    if time.monotonic() - last_render_update > 0.1:
        update_ux.update_wifi_render()
        last_render_update = time.monotonic()
    update_ux.render_wifi()
update_ux.change_builtin_neopixel_status(is_enabled=False)

# Actually connect
import wifi
from secrets import secrets

tries = 0
error = ""
while tries < 3:
    try:
        wifi.radio.connect(secrets["ssid"], secrets["password"])
    except Exception as e:
        start_time = time.monotonic()
        update_ux.change_builtin_neopixel_status(is_enabled=True)
        while time.monotonic() - start_time < 5:
            update_ux.wifi_trying_again(start_time, 5)
        update_ux.change_builtin_neopixel_status(is_enabled=False)
        tries += 1
        error = e
    else:
        break
if tries == 3:
    update_ux.display_image("wifi_error")
    time.sleep(5)
    raise error

# Download animation
start_time = time.monotonic()
last_render_update = time.monotonic()
update_ux.change_builtin_neopixel_status(is_enabled=True)
while time.monotonic() - start_time < 5:
    if time.monotonic() - last_render_update > 0.1:
        update_ux.update_download_render()
        last_render_update = time.monotonic()
    update_ux.render_download()
update_ux.change_builtin_neopixel_status(is_enabled=False)

# Actually download
import socketpool
import ssl
import adafruit_requests

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

all_files = ["boot.py", "code.py", "update.py", "update_ux.py"]
content_of_files = {}

for file in all_files:
    content_of_files[file] = requests.get(
        f"https://raw.githubusercontent.com/KTibow/fridge/main/{file}"
    ).text

# Save animation
start_time = time.monotonic()
last_render_update = time.monotonic()
update_ux.change_builtin_neopixel_status(is_enabled=True)
while time.monotonic() - start_time < 5:
    if time.monotonic() - last_render_update > 0.1:
        update_ux.update_save_render()
        last_render_update = time.monotonic()
    update_ux.render_save()
update_ux.change_builtin_neopixel_status(is_enabled=False)

# Actually save
import json

print(json.dumps(content_of_files))
update_ux.display_image("updates_complete")
