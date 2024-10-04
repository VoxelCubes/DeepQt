from copy import deepcopy

import PySide6.QtCore as Qc
import PySide6.QtWidgets as Qw
from PySide6.QtCore import Signal

import deepqt.config as cfg
import deepqt.constants as ct
import deepqt.gui_utils as gu
import deepqt.utils as ut
from deepqt.gui_utils import show_info
from deepqt.ui_generated_files.ui_backend_configuration import Ui_BackendConfiguration


class BackendConfiguration(Qw.QDialog, Ui_BackendConfiguration):
    """
    An overview of all available backends and their settings.
    This creates a deepcopy of the config to avoid modifying the original
    when cancelling changes.
    """

    config: cfg.Config
    debug: bool
    theme_is_dark: ut.Shared[bool]

    def __init__(
        self,
        parent,
        config: cfg.Config,
        debug: bool,
        theme_is_dark: ut.Shared[bool],
        theme_changed: Signal,
    ) -> None:
        # Don't pass the parent due to a bug in PySide6.
        Qw.QDialog.__init__(self)
        self.setupUi(self)
        self.config = deepcopy(config)
        self.debug = debug
        self.theme_is_dark = theme_is_dark

        self.init_custom_icons()
        self.populate_backend_list()
        self.style_backend_list()
        self.style_backend_list_font()
        self.increase_heading_font_size()

        theme_changed.connect(self.init_custom_icons)
        theme_changed.connect(self.style_backend_list)

        self.listWidget_backends.currentItemChanged.connect(self.on_backend_selected)
        self.select_current_backend()

        self.buttonBox.button(Qw.QDialogButtonBox.RestoreDefaults).clicked.connect(
            self.reset_to_defaults
        )

    def get_modified_config(self) -> cfg.Config:
        """
        For exporting the copied, likely modified config.

        :return: The modified config.
        """
        return self.config

    def init_custom_icons(self) -> None:
        # This may need to be reloaded if the theme changes.
        self.label_reliability_icon.setToolTip("This backend requires per-segment supervision.")
        self.label_cost_icon.setToolTip("This backend may incur costs.")
        if self.theme_is_dark.get():
            style = "dark"
        else:
            style = "light"
        self.label_reliability_icon.setPixmap(
            gu.load_custom_icon("unreliable-service", style).pixmap(24)
        )
        self.label_cost_icon.setPixmap(gu.load_custom_icon("cost-warning", style).pixmap(24))

    def populate_backend_list(self) -> None:
        # If debugging, show debug backends as well.
        available_backends = list(ct.Backend)
        if not self.debug:
            available_backends = [b for b in available_backends if b not in ct.debug_backends]

        for backend in available_backends:
            self.add_backend_to_list(ct.Backend(backend))

    def style_backend_list(self) -> None:
        """
        Make the icons, as well as some internal padding
        to give some vertical space for the highlight.
        Also removing the shaded background from the list.

        This needs to be reapplied when the palette changes.
        """
        self.listWidget_backends.setIconSize(Qc.QSize(32, 32))
        self.listWidget_backends.setStyleSheet(
            """
            QListView::item {
                padding: 2px;
                color: palette(Text);
            }
            QListWidget {
                background-color: transparent;
            }
            """
        )

    def style_backend_list_font(self) -> None:
        # Separately scale the font, so that this isn't readjusted each
        # time the theme changes, causing the font to grow indefinitely.
        current_font = self.listWidget_backends.font()
        current_font.setPointSize(round(current_font.pointSize() * 1.2))
        self.listWidget_backends.setFont(current_font)

    def increase_heading_font_size(self) -> None:
        current_font = self.label_backend_name.font()
        current_font.setPointSize(current_font.pointSize() * 2)
        self.label_backend_name.setFont(current_font)

    def add_backend_to_list(self, backend: ct.Backend) -> None:
        backend_conf = self.config.backend_configs[backend]
        self.listWidget_backends.addIconTextItemLinkedData(
            backend_conf.load_icon(), backend_conf.name, backend
        )

    def select_current_backend(self) -> None:
        current_backend = self.config.current_backend
        self.listWidget_backends.setCurrentIndexByLinkedData(current_backend)

    def on_backend_selected(self) -> None:
        selected_backend = self.listWidget_backends.currentLinkedData()
        self.show_backend(selected_backend)

    def show_backend(self, backend: ct.Backend) -> None:
        """
        Load the current backend's settings into the dialog.
        This also sets what the current backend is when closing the dialog.

        :param backend: The backend to show.
        """
        self.config.current_backend = backend
        backend_conf = self.config.backend_configs[backend]
        self.label_backend_name.setText(backend_conf.name)
        self.label_icon.setPixmap(backend_conf.load_icon().pixmap(64))
        self.label_description.setText(backend_conf.description)
        self.label_reliability_icon.setVisible(backend_conf.unreliable)

        if backend_conf.help:
            self.buttonBox.addButton(Qw.QDialogButtonBox.Help)
            self.buttonBox.button(Qw.QDialogButtonBox.Help).clicked.connect(
                lambda: gu.show_info(self, "Info", backend_conf.help)
            )
        else:
            self.buttonBox.removeButton(self.buttonBox.button(Qw.QDialogButtonBox.Help))

        self.label_cost_icon.setVisible(backend_conf.paid)

        self.backend_settings.load_backend(backend_conf)

    def reset_to_defaults(self) -> None:
        """
        This deletes and creates a new backend config object for the current backend.
        """
        selected_backend = self.listWidget_backends.currentLinkedData()
        new_backend_conf = cfg.backend_to_config[selected_backend]()
        self.config.backend_configs[selected_backend] = new_backend_conf
        self.show_backend(selected_backend)
        show_info(
            self,
            "Settings Reset",
            f"The settings for {new_backend_conf.name} have been reset to their default values.",
        )
