import platform
import subprocess
from pathlib import Path

import PySide6.QtWidgets as Qw
from logzero import logger


def show_critical(parent, title: str, msg: str):
    return Qw.QMessageBox.critical(parent, title, msg, Qw.QMessageBox.Yes, Qw.QMessageBox.Abort)


def show_warning(parent, title: str, msg: str):
    Qw.QMessageBox.warning(parent, title, msg, Qw.QMessageBox.Ok)


def show_info(parent, title: str, msg: str):
    Qw.QMessageBox.information(parent, title, msg, Qw.QMessageBox.Ok)


def show_question(parent, title: str, msg: str) -> bool:
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
    For large numbers, write with a K suffix and
    provide 1 decimal place, if it is needed.
    Separate the thousands with a comma.

    :param count: Count to format.
    :return: Formatted string.
    """
    if count < 10_000:
        return str(count)
    else:
        rounded = round(count / 1_000, 1)
        if rounded == int(rounded):
            return f"{int(rounded):n}K"
        else:
            # return f"{rounded}K"
            return f"{rounded:n}K"


def f_plural(value, singular: str, plural: str):
    """
    Selects which form to use based on the value.
    """
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
        return f"{seconds} {f_plural(seconds, 'second', 'seconds')}"
    elif seconds < 60 * 60:
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes} {f_plural(minutes, 'minute', 'minutes')} {seconds} {f_plural(seconds, 'second', 'seconds')}"
    else:
        hours = seconds // (60 * 60)
        minutes = (seconds % (60 * 60)) // 60
        return (
            f"{hours} {f_plural(hours, 'hour', 'hours')} "
            f"{minutes} {f_plural(minutes, 'minute', 'minutes')}"
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


def weighted_average(old_value: float, new_value: float, weight: float = 0.25) -> float:
    """
    Calculate a weighted average.
    When chained several times, it's an exponential moving average.
    """
    return old_value * (1 - weight) + new_value * weight
