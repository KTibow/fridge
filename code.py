try:
    import os
    os.stat("/latest_boot.py")
    with open("/boot.py", "w") as boot:
        with open("/latest_boot.py", "r") as new_boot:
            pass
except Exception:
    pass
