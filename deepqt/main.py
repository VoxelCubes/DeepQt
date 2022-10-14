import os
import sys
import argparse
import platform

import PySide6.QtWidgets as Qw
import PySide6.QtGui as Qg
import PySide6.QtCore as Qc
import logzero
from logzero import logger

import deepqt.config as cfg
from deepqt.driver_mainwindow import MainWindow
from deepqt import __program__, __version__, __description__

# TODO Testing

import deepqt.rc_generated_files.fallback_icons_rc


def main():
    # Parse command line arguments
    # args:
    #   --mock: Pretend to translate but don't actually use the API.
    #   --debug-api: Show DeepL API debug messages.
    #   --quieter-logs: Don't log debug messages.
    #   --icon-theme: Use the specified icon theme. Included are "Breeze" and "BreezeDark". Default to system theme.
    #   -v --version: Show version.

    parser = argparse.ArgumentParser(description=__description__, prog=__program__)
    parser.add_argument("--mock", action="store_true", help="Use the deepl mock server on localhost:3000.")
    parser.add_argument("--debug-api", action="store_true", help="Show DeepL API debug messages.")
    parser.add_argument("--quieter-logs", action="store_true", help="Don't log debug messages.")
    parser.add_argument(
        "--icon-theme",
        choices=["Breeze", "BreezeDark"],
        default=None,
        help='Use the specified icon theme. Included are "Breeze" and "BreezeDark". Default to system theme.',
    )
    parser.add_argument("-v", "--version", action="version", version=f"{__program__} {__version__}")

    args = parser.parse_args()

    # Set up logging.
    if args.quieter_logs:
        logzero.loglevel(logzero.INFO)
    else:
        logzero.loglevel(logzero.DEBUG)

    cfg.log_path().parent.mkdir(parents=True, exist_ok=True)
    # Log up to 200KB to the log file.
    logzero.logfile(str(cfg.log_path()), maxBytes=200 * 2**10, backupCount=1, loglevel=logzero.DEBUG)
    logger.info("---- Starting up ----")
    logger.info(f"Log file is {cfg.log_path()}")

    if args.debug_api:
        import logging

        logger.info("Enabled debugging network requests.")
        logging.basicConfig()
        logging.getLogger("deepl").setLevel(logging.DEBUG)

    Qw.QApplication.setAttribute(Qc.Qt.AA_EnableHighDpiScaling, True)

    # Set up icon theme.
    if args.icon_theme:
        if args.icon_theme == "Breeze":
            logger.info("Using Breeze icon theme.")
            Qg.QIcon.setThemeName("Breeze")
        elif args.icon_theme == "BreezeDark":
            logger.info("Using BreezeDark icon theme.")
            Qg.QIcon.setThemeName("BreezeDark")
        else:
            raise ValueError(f"Unknown icon theme: {args.icon_theme}")
    elif platform.system() == "Windows":
        # Default to Breeze on Windows.
        logger.info("Using Breeze icon theme.")
        Qg.QIcon.setThemeName("Breeze")

    # Start the main window.
    app = Qw.QApplication(sys.argv)

    try:
        window = MainWindow(args.mock)
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        logger.exception(
            e,
        )
    finally:
        logger.info("---- Shutting down ----\n")


if __name__ == "__main__":
    main()
