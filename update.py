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
    update_ux.display_image("wifi_error")
