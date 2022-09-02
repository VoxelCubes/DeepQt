import os
import sys
import argparse

import PySide6.QtWidgets as Qw
import logzero
from logzero import logger

import deepqt.config as cfg
from deepqt.driver_mainwindow import MainWindow
from deepqt import __program__, __version__, __description__

# TODO support ODS files
# TODO maybe support csv files
# TODO maybe port away from openpyxl to only pyexcel
# TODO documentation
# TODO epub files
# TODO Testing


def main():
    # Parse command line arguments
    # args:
    #   --mock: Use the deepl mock server on localhost:3000.
    #   --debug-api: Show DeepL API debug messages.
    #   --quieter-logs: Don't log debug messages.

    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("--mock", action="store_true", help="Use the deepl mock server on localhost:3000.")
    parser.add_argument("--debug-api", action="store_true", help="Show DeepL API debug messages.")
    parser.add_argument("--quieter-logs", action="store_true", help="Don't log debug messages.")
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

    if args.mock:
        logger.info("Mock server enabled.")
        os.environ["DEEPL_MOCK_SERVER_PORT"] = "3000"
        os.environ["DEEPL_MOCK_PROXY_SERVER_PORT"] = "3001"
        os.environ["DEEPL_SERVER_URL"] = "http://localhost:3000"
        os.environ["DEEPL_PROXY_URL"] = "http://localhost:3001"

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
