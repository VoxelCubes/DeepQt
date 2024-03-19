import argparse
import platform
import sys

import PySide6.QtGui as Qg
import PySide6.QtWidgets as Qw
from loguru import logger

import deepqt.utils as ut
from deepqt import __program__, __display_name__, __version__, __description__
from deepqt.constants import Command, Backend
from deepqt.driver_mainwindow import MainWindow


# TODO Testing


def main():
    # Parse command line arguments.
    parser = argparse.ArgumentParser(
        description=__description__,
        prog=__display_name__,
        epilog="Example usage:\n"
        f"  {__program__} \t\t\t\t\t\t| to simply launch the GUI\n"
        f"  {__program__} {Command.FILES.value} file1.txt ebook2.epub --translate-now \t| to immediately start translating the given files\n"
        f'  {__program__} {Command.TEXT.value} "Hello world" --api=deepl \t\t| to pre-fill the given text into the interactive session and select the deepl api\n'
        f"  {__program__} {Command.CLIPBOARD.value} \t\t\t\t\t| to pre-fill the current clipboard text in the interactive session\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=False,
        help="Optionally launch the GUI with files or text on startup:",
    )

    parser_files = subparsers.add_parser("files", help="Translate files. Usage: files file1.txt file2.txt [--options]")
    parser_files.add_argument("file", nargs="+", help="Files to translate")

    parser_text = subparsers.add_parser("text", help="Translate text. Usage: text 'Your text here' [--options]")
    parser_text.add_argument("text", help="Text to translate")

    parser_clipboard = subparsers.add_parser(
        "clipboard", help="Translate text from clipboard. Usage: clipboard [--options]"
    )

    supported_backends = [b.value for b in Backend]

    # Common arguments
    for p in [parser_files, parser_text, parser_clipboard, parser]:
        p.add_argument("--translate-now", "-n", action="store_true", help="Translate immediately at startup")
        p.add_argument(
            "--api",
            "-a",
            choices=supported_backends,
            default=None,
            help="The translation API to use",
        )
        p.add_argument("--debug-api", "-D", action="store_true", help="Enable debug messages for the APIs")
        p.add_argument("--debug", "-d", action="store_true", help="Enable debug mode")
        p.add_argument("--version", "-v", action="version", version=f"{__display_name__} {__version__}")

    args = parser.parse_args()

    ut.get_log_path().parent.mkdir(parents=True, exist_ok=True)
    # Log up to 10MB to the log file.
    logger.add(str(ut.get_log_path()), rotation="10 MB", retention="1 week", level="DEBUG")

    logger.info(ut.collect_system_info(__file__))

    # When bundling an executable, stdout can be None if no console is supplied.
    if sys.stdout is not None:
        if args.debug:
            logger.add(sys.stdout, level="DEBUG")
        else:
            logger.add(sys.stdout, level="WARNING")

    if args.debug_api:
        import logging

        logger.info("Enabled debugging network requests.")
        logging.basicConfig()
        logging.getLogger("deepl").setLevel(logging.DEBUG)

    # Dump the command line arguments if in debug mode.
    if args.debug:
        logger.debug(f"Launch arguments: {args}")

    # Start Qt runtime.
    app = Qw.QApplication(sys.argv)

    Qg.QIcon.setFallbackSearchPaths([":/icons", ":/icon-themes"])
    # We need to set an initial theme on Windows, otherwise the icons will fail to load
    # later on, even when switching the theme again.
    if platform.system() == "Windows" or ut.running_in_flatpak():
        Qg.QIcon.setThemeName("breeze")
        Qg.QIcon.setThemeSearchPaths([":/icons", ":/icon-themes"])

    command = Command(args.command)
    inputs = None
    if command == Command.FILES:
        inputs = args.file
    elif command == Command.TEXT:
        inputs = args.text

    try:
        window = MainWindow(command, inputs, args.api, args.translate_now, args.debug)
        window.show()
        sys.exit(app.exec())
    except Exception:
        logger.opt(exception=True).critical("Failed to initialize the main window.")
    finally:
        logger.info(ut.SHUTDOWN_MESSAGE + "\n")


if __name__ == "__main__":
    main()
