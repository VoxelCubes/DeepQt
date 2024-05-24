from typing import assert_never

import PySide6.QtCore as Qc
import PySide6.QtWidgets as Qw
import PySide6.QtGui as Qg
from loguru import logger

import deepqt.utils as ut
import deepqt.backends.backend_interface as bi
from deepqt.ui_generated_files.ui_api_status_usage import Ui_APIStatusUsage


class APIStatusUsage(Qw.QWidget, Ui_APIStatusUsage):
    """
    Displays the status of the API connection and the remaining usage,
    only if that information is provided.

    The warn_percentile should be configured externally.
    """

    warn_percentile: int = 90

    def __init__(self, parent) -> None:
        Qw.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.load_icons()

        self.show_status(None)

    def changeEvent(self, event) -> None:
        if event.type() == Qc.QEvent.PaletteChange:
            self.load_icons()

    def load_icons(self) -> None:
        self.label_status_good_icon.setPixmap(
            Qg.QIcon.fromTheme("state-ok").pixmap(Qc.QSize(16, 16))
        )
        self.label_status_bad_icon.setPixmap(
            Qg.QIcon.fromTheme("state-error").pixmap(Qc.QSize(16, 16))
        )
        self.label_status_offline_icon.setPixmap(
            Qg.QIcon.fromTheme("data-offline").pixmap(Qc.QSize(16, 16))
        )
        self.label_usage_error_icon.setPixmap(
            Qg.QIcon.fromTheme("data-error").pixmap(Qc.QSize(16, 16))
        )
        self.label_usage_warn_icon.setPixmap(
            Qg.QIcon.fromTheme("data-warning").pixmap(Qc.QSize(16, 16))
        )

    def show_status(self, status: bi.BackendStatus | None) -> None:
        """
        The publicly facing method to show the status.

        :param status: The backend status to present.
        """
        if status is None:
            self.show_status(bi.BackendStatus(bi.ConnectionStatus.Error, None, None))
            return

        self._show_connection(status.connection)
        self._show_usage(status.usage_count, status.usage_limit)

    def _show_connection(self, status: bi.ConnectionStatus) -> None:
        connected = False
        offline = False
        error = False

        if status == bi.ConnectionStatus.Connected:
            connected = True
        elif status == bi.ConnectionStatus.Error:
            error = True
        elif status == bi.ConnectionStatus.Offline:
            offline = True
        else:
            assert_never(status)

        self.label_status_good.setVisible(connected)
        self.label_status_good_icon.setVisible(connected)
        self.label_status_bad.setVisible(error)
        self.label_status_bad_icon.setVisible(error)
        self.label_status_offline.setVisible(offline)
        self.label_status_offline_icon.setVisible(offline)

    def _show_usage(self, usage_count: int | None, usage_limit: int | None) -> None:
        # When the count is none, the usage is not applicable and therefore hidden.
        if usage_count is None:
            self.widget_usage_field.hide()
            self.label_usage_label.hide()
            self.widget_usage_field.setMaximumHeight(0)
            self.label_usage_label.setMaximumHeight(0)
            return
        else:
            self.widget_usage_field.show()
            self.label_usage_label.show()
            self.widget_usage_field.setMaximumHeight(16777215)
            self.label_usage_label.setMaximumHeight(16777215)

        # The limit can be none when the API has no upper limit (e.g. DeepL Pro, local models etc.)
        count_str = ut.format_char_count(usage_count)
        if usage_limit is None:
            count_str = ut.format_char_count(usage_count)
            usage_str = f"{count_str} {ut.f_plural(usage_count, 'character')} / Unlimited"
        else:
            percentage = usage_count / usage_limit * 100 if usage_limit > 0 else 0
            limit_str = ut.format_char_count(usage_limit)
            usage_str = f"{percentage:.2f}%  {count_str} / {limit_str} {ut.f_plural(usage_limit, 'character')}"

            if percentage < self.warn_percentile:
                self.label_usage_warn_icon.hide()
                self.label_usage_error_icon.hide()
            elif percentage < 100:
                self.label_usage_warn_icon.show()
                self.label_usage_error_icon.hide()
            else:
                self.label_usage_warn_icon.hide()
                self.label_usage_error_icon.show()

        self.label_usage.setText(usage_str)
