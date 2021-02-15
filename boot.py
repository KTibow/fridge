import digitalio
import board
should_update = False
for button in [board.D11, board.D12, board.D14, board.D15]:
    button = digitalio.DigitalInOut(button)
    button.switch_to_input()
    button.pull = digitalio.Pull.UP
    if not button.value:
        should_update = True
if should_update:
    import update
