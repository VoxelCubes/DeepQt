import os
import sys

import PySide6.QtWidgets as Qw
import logzero
from logzero import logger

import deepq.config as cfg
from driver_mainwindow import MainWindow

# TODO Time estimates
# TODO support ODS files
# TODO maybe support csv files
# TODO maybe port away from openpyxl to only pyexcel
# TODO documentation
# TODO epub files
# TODO Testing


def main():
    # Set up logging.
    if "--quiet" in sys.argv:
        logzero.loglevel(logzero.INFO)
    else:
        logzero.loglevel(logzero.DEBUG)

    cfg.log_path().parent.mkdir(parents=True, exist_ok=True)
    # Log up to 200KB to the log file.
    logzero.logfile(str(cfg.log_path()), maxBytes=200 * 2**10, backupCount=1, loglevel=logzero.DEBUG)
    logger.info("---- Starting up ----")
    logger.info(f"Log file is {cfg.log_path()}")

    if "--debug-api" in sys.argv:
        import logging

        logger.info("Enabled debugging network requests.")
        logging.basicConfig()
        logging.getLogger("deepl").setLevel(logging.DEBUG)

    # Set debug environment variables if "--mock" is passed as an argument.
    mock = "--mock" in sys.argv
    # Set up the mock server.
    if mock:
        logger.info("Mock server enabled.")
        os.environ["DEEPL_MOCK_SERVER_PORT"] = "3000"
        os.environ["DEEPL_MOCK_PROXY_SERVER_PORT"] = "3001"
        os.environ["DEEPL_SERVER_URL"] = "http://localhost:3000"
        os.environ["DEEPL_PROXY_URL"] = "http://localhost:3001"

    app = Qw.QApplication(sys.argv)

    try:
        window = MainWindow(mock)
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
