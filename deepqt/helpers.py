import platform
import subprocess
import zipfile as zf
from pathlib import Path

import PySide6.QtWidgets as Qw
from logzero import logger


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


def open_file(path: Path):
    """
    Open any given file with the default application.
    """
    logger.info(f"Opening file {path}")
    try:
        if platform.system() == "Linux":
            subprocess.run(["xdg-open", path])
        elif platform.system() == "Windows":
            subprocess.run(["start", path])
        elif platform.system() == "Darwin":
            subprocess.run(["open", path])
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
