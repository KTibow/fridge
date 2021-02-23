try:
    import os
    os.stat("/latest_boot.py")
    with open("/boot.py", "w") as boot:
        with open("/latest_boot.py", "r") as new_boot:
            boot.write(new_boot.read())
            boot.flush()
except Exception:
    pass
