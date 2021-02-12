import time
import math


def initial_load(offset_1, offset_2, offset_3, speed, magtag):
    initial_time = time.monotonic()
    while time.monotonic() - initial_time < speed:
        for i in range(4):
            color = (time.monotonic() - initial_time) * (4 / speed) + (i - 3)
            if color < 0:
                color = 0
            if color > 1:
                color = 1
            magtag.peripherals.neopixels[i] = (
                color * offset_1,
                color * offset_2,
                color * offset_3,
            )


def countdown(offset_1, offset_2, offset_3, speed, magtag, eval_function=lambda: None):
    for i in range(4):
        initial_time = time.monotonic()
        while time.monotonic() - initial_time < speed / 4:
            j = (time.monotonic() - initial_time) * -1 + (speed / 4)
            magtag.peripherals.neopixels[i] = (j * offset_1, j * offset_2, j * offset_3)
            response = eval_function()
            if response is not None:
                return response


def sin_animate(offset_1, offset_2, offset_3, start_pixel, stop_pixel, magtag):
    for i in range(start_pixel, stop_pixel):
        color = (math.sin(time.monotonic() * 2 + i) + 2) / 3
        magtag.peripherals.neopixels[i] = (
            color * offset_1,
            color * offset_2,
            color * offset_3,
        )
