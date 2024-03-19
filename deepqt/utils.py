import difflib
import os
import platform
import shutil
import subprocess
import sys
import zipfile as zf
from io import StringIO
from pathlib import Path

import PySide6
import PySide6.QtCore as Qc
import PySide6.QtGui as Qg
import PySide6.QtWidgets as Qw
from loguru import logger
from xdg import XDG_CONFIG_HOME, XDG_CACHE_HOME

from deepqt import __program__, __version__


# Logging session markers.
STARTUP_MESSAGE = "---- Starting up ----"
SHUTDOWN_MESSAGE = "---- Shutting down ----"


def running_in_flatpak() -> bool:
    return Path("/.flatpak-info").exists()


def collect_system_info(callers_file: str) -> str:
    buffer = StringIO()
    buffer.write("\n" + STARTUP_MESSAGE)
    buffer.write("\n- Program Information -\n")
    buffer.write(f"Program: {__program__} {__version__}\n")
    buffer.write(f"Executing from: {callers_file}\n")
    buffer.write(f"Log file: {get_log_path()}\n")
    buffer.write(f"Config file: {get_config_path()}\n")
    buffer.write(f"Cache directory: {get_cache_path()}\n")
    buffer.write("- System Information -\n")
    buffer.write(f"Operating System: {platform.system()} {platform.release()}\n")
    if platform.system() == "Linux":
        buffer.write(f"Desktop Environment: {os.getenv('XDG_CURRENT_DESKTOP', 'unknown')}\n")
    if running_in_flatpak():
        buffer.write("Sandbox: Running in Flatpak\n")
    buffer.write(f"Machine: {platform.machine()}\n")
    buffer.write(f"Python Version: {sys.version}\n")
    buffer.write(f"PySide (Qt) Version: {PySide6.__version__}\n")
    buffer.write(f"Available Qt Themes: {', '.join(Qw.QStyleFactory.keys())}\n")
    buffer.write(f"System locale: {Qc.QLocale.system().name()}\n")
    buffer.write(f"CPU Cores: {os.cpu_count()}\n")

    return buffer.getvalue()


def get_config_path() -> Path:
    """
    Get the path to the configuration file for both Linux and Windows.
    """
    xdg_path = os.getenv("XDG_CONFIG_HOME") or Path.home() / ".config"

    if platform.system() == "Linux":
        path = Path(XDG_CONFIG_HOME, __program__, __program__ + "rc")
    elif platform.system() == "Windows":
        path = Path(
            xdg_path if "XDG_CONFIG_HOME" in os.environ else os.getenv("APPDATA"),
            __program__,
            __program__ + "config.ini",
        )
    elif platform.system() == "Darwin":
        path = Path(
            xdg_path if "XDG_CONFIG_HOME" in os.environ else (Path.home() / "Library" / "Application Support"),
            __program__,
            __program__ + "config.ini",
        )
    else:  # ???
        raise NotImplementedError("Your OS is currently not supported.")

    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def get_cache_path() -> Path:
    """
    Get the default suggested path to the cache directory for both Linux and Windows.
    """
    xdg_path = os.getenv("XDG_CACHE_HOME") or Path.home() / ".cache"

    if platform.system() == "Linux":
        path = Path(XDG_CACHE_HOME, __program__)
    elif platform.system() == "Windows":
        path = Path(
            xdg_path if "XDG_CACHE_HOME" in os.environ else os.getenv("APPDATA"),
            __program__,
            "cache",
        )
    elif platform.system() == "Darwin":
        path = Path(
            xdg_path if "XDG_CACHE_HOME" in os.environ else (Path.home() / "Library" / "Caches"),
            __program__,
        )
    else:  # ???
        raise NotImplementedError("Your OS is currently not supported.")

    path.mkdir(parents=True, exist_ok=True)
    return path


def get_log_path() -> Path:
    """
    Get the path to the log file.
    Use the cache directory for this.
    """
    return get_cache_path() / f"{__program__}.log"


def get_lock_file_path() -> Path:
    """
    Get the path to the lock file.
    Use the cache directory for this.
    """
    return get_cache_path() / f"{__program__}.lock"


def open_file_with_editor(path: Path, configured_opener: str | None) -> None:
    """
    Open the given file with the given editor.
    If no editor is given, use the default editor for the current OS.

    :param path: The path to the file to open.
    :param configured_opener: The configured editor to use.
    """
    if platform.system() == "Linux":
        opener = "xdg-open" if configured_opener is None else configured_opener
        print(f"Opening {path} with {opener}.")
        # Test if the configured editor exists. Even xdg-open may be missing, like in a docker container.
        if shutil.which(opener) is None:
            print(
                f"Configured editor '{opener}' not found. "
                f"Please open the file manually or configure another program."
            )
            return
        # Run and detach the process, so this one can exit.
        subprocess.Popen([opener, path], start_new_session=True)

        print("If nothing happens, try setting the profile_editor option in the config.")

    elif platform.system() == "Windows":
        opener = "start" if configured_opener is None else configured_opener
        print(f"Opening {path} with {opener}.")
        os.system(f"{opener} {path}")

        print("\nIf nothing happens, try setting the 'profile_editor' option in the config.")
    elif platform.system() == "Darwin":
        opener = "open" if configured_opener is None else configured_opener
        print(f"Opening {path} with {opener}.")
        os.system(f"{opener} {path}")

        print("\nIf nothing happens, try setting the 'profile_editor' option in the config.")
    else:
        print(
            f"Your OS ({platform.system()}) is not supported, but you can open the path manually:\n"
            f"Profile path: {path}"
        )


def empty_cache_dir(cache_dir: Path) -> None:
    """
    Empty the cache directory.
    Only attempt to delete .png images and .json files.
    Or .pt and .onnx files for PyTorch and ONNX models.
    This limits the damage if this points to the wrong directory.
    """
    for item in cache_dir.iterdir():
        if item.suffix in [".png", ".json", ".pt", ".onnx"]:
            item.unlink()


def closest_match(word: str, choices: list[str]) -> str | None:
    """
    Return the closest match for the given word in the list of choices.
    If no good match is found, return None.
    """
    if word in choices:
        return word
    else:
        # Find the closest match using difflib:
        closest = difflib.get_close_matches(word, choices, 1, 0.5)  # 0.6 is the default threshold
        if closest:
            return str(closest[0])
        else:
            return None


# For all show functions, pad the dialog message, so that the dialog is not too narrow for the window title.
MIN_MSG_LENGTH = 50


def show_critical(parent, title: str, msg: str):
    msg = msg.ljust(MIN_MSG_LENGTH)
    return Qw.QMessageBox.critical(parent, title, msg, Qw.QMessageBox.Yes, Qw.QMessageBox.Abort)


def show_warning(parent, title: str, msg: str):
    msg = msg.ljust(MIN_MSG_LENGTH)
    Qw.QMessageBox.warning(parent, title, msg, Qw.QMessageBox.Ok)


def show_info(parent, title: str, msg: str):
    msg = msg.ljust(MIN_MSG_LENGTH)
    Qw.QMessageBox.information(parent, title, msg, Qw.QMessageBox.Ok)


def show_question(parent, title: str, msg: str) -> bool:
    msg = msg.ljust(MIN_MSG_LENGTH)
    dlg = Qw.QMessageBox(parent)
    dlg.setWindowTitle(title)
    dlg.setText(msg)
    dlg.setStandardButtons(Qw.QMessageBox.Yes | Qw.QMessageBox.Cancel)
    dlg.setIcon(Qw.QMessageBox.Question)
    response = dlg.exec()

    return response == Qw.QMessageBox.Yes


def format_char_count(count: int) -> str:
    """
    Format the count to be more human readable.
    For large numbers, write with a K suffix and provide 1 decimal place, if it is needed.
    Separate the thousands with a comma.
    Should it be necessary, use the M suffix for millions.

    :param count: Count to format.
    :return: Formatted string.
    """
    if count < 1_000:
        return str(count)
    elif count < 1_000_000:
        rounded = round(count / 1_000, 1)
        if rounded == int(rounded):
            return f"{int(rounded):n}K"
        else:
            return f"{rounded:n}K"
    else:
        rounded = round(count / 1_000_000, 1)
        if rounded == int(rounded):
            return f"{int(rounded):n}M"
        else:
            return f"{rounded:n}M"


def f_plural(value, singular: str, plural: str = "") -> str:
    """
    Selects which form to use based on the value.

    :param value: Value to check.
    :param singular: Singular form.
    :param plural: (Optional) Plural form. If not given, the singular form is used with an 's' appended.
    :return: The appropriate form.
    """
    if not plural:
        plural = singular + "s"
    return singular if value == 1 else plural


def f_time(seconds: int) -> str:
    """
    Format a time in seconds to a human readable string.
    Return a format like:
    1 second
    2 minutes 3 seconds
    4 hours 5 minutes
    """
    if seconds < 60:
        return f"{seconds} {f_plural(seconds, 'second')}"
    elif seconds < 60 * 60:
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes} {f_plural(minutes, 'minute')} {seconds} {f_plural(seconds, 'second')}"
    else:
        hours = seconds // (60 * 60)
        minutes = (seconds % (60 * 60)) // 60
        return (
            f"{hours} {f_plural(hours, 'hour')} "
            f"{minutes} {f_plural(minutes, 'minute')}"
            f"   [You're batshit insane!]"
        )


def open_file(path: Path) -> None:
    """
    Open any given file with the default application.
    """
    logger.info(f"Opening file {path}")
    try:
        # Use Qt to open the file, so that it works on all platforms.
        Qg.QDesktopServices.openUrl(Qc.QUrl.fromLocalFile(str(path)))
    except Exception as e:
        logger.exception(e)


def ensure_unique_file_path(file_path: Path) -> Path:
    """
    Ensure that the file path is unique.
    If the file already exists, append a number to the file name,
    incrementing it until a unique file path is found.
    """
    counter = 1
    output_file_path = file_path
    while output_file_path.exists():
        output_file_path = file_path.parent / (file_path.stem + "_" + str(counter) + file_path.suffix)
        counter += 1
    return output_file_path


def weighted_average(old_value: float, new_value: float, weight: float = 0.25) -> float:
    """
    Calculate a weighted average.
    When chained several times, it's an exponential moving average.
    """
    return old_value * (1 - weight) + new_value * weight


def nuke_folder_contents(folder_path: Path):
    """
    Delete all files and folders in the given folder.
    """
    for child in folder_path.iterdir():
        if child.is_dir():
            nuke_folder_contents(child)
            child.rmdir()
        else:
            child.unlink()


def zip_folder_to_epub(folder_unzipped: Path, destination: Path) -> bool:
    """
    Zip a folder to an epub file.

    :param folder_unzipped: Path to the folder to zip.
    :param destination: Path to the destination file.
    :return: True if successful, False otherwise.
    """
    seen = set()

    def add_to_zip(zip_file: zf.ZipFile, path: Path):
        """
        Add a file or folder to the zip file.
        """
        if path in seen:
            return
        seen.add(path)
        if path.is_dir():
            for child in path.iterdir():
                add_to_zip(zip_file, child)
        # Add everything else that isn't junk.
        elif not path.name.endswith("Thumbs.db") and not path.name.endswith("debug.log"):
            zip_file.write(path, path.relative_to(folder_unzipped))

    # Check that this was probably an epub file.
    if (folder_unzipped / "mimetype").is_file() and (folder_unzipped / "META-INF").is_dir():
        # Start the epub file with the mimetype file.
        with zf.ZipFile(destination, "w", compression=zf.ZIP_DEFLATED) as myzip:
            add_to_zip(myzip, folder_unzipped / "mimetype")

        # Append the META-INF folder.
        with zf.ZipFile(destination, "a", compression=zf.ZIP_DEFLATED) as myzip:
            add_to_zip(myzip, folder_unzipped / "META-INF")

        # Append the rest of the files.
        with zf.ZipFile(destination, "a", compression=zf.ZIP_DEFLATED) as myzip:
            for file in folder_unzipped.iterdir():
                add_to_zip(myzip, file)

        return True
    else:
        logger.error(f"Folder {folder_unzipped} is missing mimetype and/or META-INF folder.")
        return False
