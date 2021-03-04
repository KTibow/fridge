import glob
import os
import shutil
import stat
import subprocess
import tempfile
import time

drive_letters = [chr(letter) for letter in range(ord("D"), ord("L"))]


def boot_out_search():
    for drive in drive_letters:
        if os.path.exists(f"{drive}:\\boot_out.txt"):
            return drive


def subprocess_search():
    for drive in drive_letters:
        try:
            if (
                "CIRCUITPY"
                in subprocess.check_output(["cmd", rf"/c vol {drive}:"]).decode()
            ):
                return drive
        except subprocess.CalledProcessError:
            pass


def handle_error(func, path, exc_info):
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)


def get_latest_version(drive):
    if os.path.exists(os.path.join(tempfile.gettempdir(), "MagTagUpdater")):
        shutil.rmtree(
            os.path.join(tempfile.gettempdir(), "MagTagUpdater"), onerror=handle_error
        )
    subprocess.call(
        [
            "git",
            "clone",
            "https://github.com/KTibow/fridge",
            os.path.join(tempfile.gettempdir(), "MagTagUpdater"),
        ]
    )
    shutil.copy(
        os.path.join(os.path.expanduser("~"), "secrets.py"),
        os.path.join(tempfile.gettempdir(), "MagTagUpdater"),
    )
    if os.path.exists(rf"{drive}:\boot_out.txt"):
        shutil.copy(
            rf"{drive}:\boot_out.txt",
            os.path.join(tempfile.gettempdir(), "MagTagUpdater"),
        )
    os.chdir(os.path.join(tempfile.gettempdir(), "MagTagUpdater"))
    # git-timestamp.sh:
    # IFS=$'\n'
    # for FILE in $(git ls-tree -r main --name-only)
    # do
    #   REV=$(git rev-list -n 1 HEAD "$FILE");
    #   STAMP=$(git show --pretty=format:%ai --abbrev-commit "$REV" | head -n 1);
    #   touch -d "$STAMP" $FILE;
    #   echo "Set $FILE to $STAMP"
    # done
    subprocess.call(
        [
            os.path.join(
                os.path.expanduser("~"), r"AppData\Local\Programs\Git\bin\bash.exe"
            ),
            r"~/git-timestamp.sh",
        ]
    )
    for trashable_dir in [".git", "leftunder_addon", "_layouts", "assets"]:
        shutil.rmtree(
            os.path.join(tempfile.gettempdir(), "MagTagUpdater", trashable_dir),
            onerror=handle_error,
        )
    for trashable_file in [
        ".gitignore",
        "README.md",
        "leftunder.svg",
        "leftunder-color.svg",
        "update_magtag.py",
        "serial.html",
    ]:
        os.remove(os.path.join(tempfile.gettempdir(), "MagTagUpdater", trashable_file))


def copy_files(drive):
    subprocess.call(
        [
            "robocopy",
            os.path.join(tempfile.gettempdir(), "MagTagUpdater"),
            drive + ":",
            "/MIR",
        ]
    )


def main():
    print("Updating.")
    print("  Searching for update target.")
    drive = boot_out_search()
    if drive is None:
        print("  boot_out.txt search failed.")
        print("  Falling back to CMD vol...")
        drive = subprocess_search()
        if drive is None:
            print("  Couldn't find drive. Press the reset button on the MagTag.")
            input("  When you're ready, press enter to try again.")
            main()
            return
    print("  Found drive", drive)
    print("Downloading updates.")
    get_latest_version(drive)
    print("Applying updates.")
    copy_files(drive)
    print("Done!")


main()
