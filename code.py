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
