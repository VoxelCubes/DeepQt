from typing import Any, Callable

import PySide6.QtWidgets as Qw
from loguru import logger

import deepqt.CustomQ.CTooltipLabel as ctl
import deepqt.backends.backend_interface as bi
import deepqt.backends.deepl_backend as db
import deepqt.constants as ct
import deepqt.key_button as kb


# If you ever find yourself placing this inside a ScrollArea again, remember this:

# Attention: this is black magic that makes the scroll area resize to the size of the widget inside it.
# For whatever stupid reason it won't do that by itself when loading the children dynamically.
# self.scrollArea.sizeHint = lambda: self.scrollArea_backend_config.sizeHint()
# self.scrollArea.updateGeometry()


class BackendOptionWidget(Qw.QHBoxLayout):
    """
    A layout widget that contains some data widget and a reset button.
    """

    attr_name: str
    _entry_type: type
    _data_widget: Qw.QWidget
    _info_widget: ctl.CTooltipLabel

    _data_setter: Callable[[Any], None]
    _data_getter: Callable[[], Any]

    def __init__(self, attr_name: str, entry_type: type, tooltip: str = "") -> None:
        super().__init__()
        self.attr_name = attr_name
        self.create_data_widget(entry_type)
        self.addWidget(self._data_widget)
        if tooltip:
            spacer = Qw.QSpacerItem(6, 6, Qw.QSizePolicy.Expanding, Qw.QSizePolicy.Minimum)
            self.addItem(spacer)
            self._info_widget = ctl.CTooltipLabel(tooltip=tooltip)
            self.addWidget(self._info_widget)
            self.setStretch(0, 1)

    def create_data_widget(self, entry_type: type) -> None:
        if entry_type == bool:
            self._data_widget: Qw.QCheckBox = Qw.QCheckBox()
            self._data_setter = self._data_widget.setChecked
            self._data_getter = self._data_widget.isChecked

        elif entry_type in (int, ct.Milliseconds, ct.Seconds):
            self._data_widget: Qw.QSpinBox = Qw.QSpinBox()
            self._data_widget.setMaximum(9999999)  # Can't go much higher due to int32 limits.
            self._data_setter = self._data_widget.setValue
            self._data_getter = self._data_widget.value
            if entry_type == ct.Milliseconds:
                self._data_widget.setSuffix(" ms")
            elif entry_type == ct.Seconds:
                self._data_widget.setSuffix(" s")

        elif entry_type in (float, ct.SecondsF):
            self._data_widget: Qw.QDoubleSpinBox = Qw.QDoubleSpinBox()
            self._data_widget.setStepType(Qw.QAbstractSpinBox.AdaptiveDecimalStepType)
            self._data_setter = self._data_widget.setValue
            # Round to 2 decimal places.
            self._data_getter = lambda: round(self._data_widget.value(), 2)
            if entry_type == ct.SecondsF:
                self._data_widget.setSuffix(" s")

        elif entry_type == ct.Percentage:
            self._data_widget: Qw.QDoubleSpinBox = Qw.QDoubleSpinBox()
            self._data_widget.setRange(0.0, 100.0)
            self._data_widget.setDecimals(1)
            self._data_widget.setSuffix("%")
            self._data_setter = self._data_widget.setValue
            self._data_getter = self._data_widget.value

        elif entry_type == str:
            self._data_widget: Qw.QLineEdit = Qw.QLineEdit()
            self._data_setter = self._data_widget.setText
            self._data_getter = self._data_widget.text

        elif entry_type == ct.APIKey:
            self._data_widget: kb.APIKeyButton = kb.APIKeyButton()
            self._data_setter = self._data_widget.set_key
            self._data_getter = self._data_widget.get_key

        elif entry_type == ct.HTML:
            raise TypeError("HTML type not supported in this context")

        else:
            raise TypeError(f"Unsupported entry type {entry_type}")

        # elif entry_type == EntryTypes.MimeSuffixIMG:
        #     # Use a spinbox and populate it with the mime suffixes from the config.
        #     # Use "Same as image" as the default value, with a linked data of None.
        #     # The other suffixes just store the suffix as the linked data.
        #     self._data_widget: CComboBox = CComboBox()
        #     self._data_widget.addTextItemLinkedData(
        #         self.tr("Same as image", "Profile default option for the file type"), None
        #     )
        #     for suffix in cfg.SUPPORTED_IMG_TYPES:
        #         self._data_widget.addTextItemLinkedData(suffix, suffix)
        #
        #     self._data_widget.currentIndexChanged.connect(self._value_changed)
        #     self._data_setter = self._data_widget.setCurrentIndexByLinkedData
        #     self._data_getter = self._data_widget.currentLinkedData

    def set_value(self, value: Any) -> None:
        self._data_setter(value)

    def get_value(self) -> Any:
        return self._data_getter()

    def set_up_key_input(self, key: ct.APIKey, help_html: ct.HTML = "") -> None:
        self._data_widget: kb.APIKeyButton
        self._data_widget.setup(key, help_html)


class BackendSettings(Qw.QWidget):
    """
    Expose settings for the backend.
    """

    layout: Qw.QFormLayout

    _data_widgets: dict[str, BackendOptionWidget]

    current_backend: bi.BackendConfig | None

    def __init__(self, parent=None) -> None:
        Qw.QWidget.__init__(self, parent)
        self.current_backend = None
        self.layout = Qw.QFormLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self._data_widgets = {}
        size_policy = Qw.QSizePolicy(Qw.QSizePolicy.Preferred, Qw.QSizePolicy.Preferred)
        self.setSizePolicy(size_policy)

    def load_backend(self, backend: bi.BackendConfig) -> None:
        """
        Load the backend settings.
        """
        logger.info(f"Loading backend settings for {backend.name}")

        if self.current_backend != backend:
            self._load_backend_structure(backend)

        self._load_backend_values(backend)

    def _load_backend_structure(self, backend: bi.BackendConfig) -> None:
        """
        Load the structure of the backend settings as widgets.
        """
        attributes: list[tuple[str, bi.AttributeMetadata]] = list(
            backend.attribute_metadata().items()
        )

        # Clear out the form layout.
        for i in reversed(range(self.layout.rowCount())):
            self.layout.removeRow(i)

        def add_attribute(
            _attribute: str, _meta: bi.AttributeMetadata, _backend: bi.BackendConfig
        ) -> BackendOptionWidget:
            widget = BackendOptionWidget(_attribute, _meta.type, _meta.description)
            # Set up key input if the attribute is an API key.
            if _meta.type == ct.APIKey:
                # Only certain APIs have API keys.
                _backend: db.DeepLConfig
                widget.set_up_key_input(_backend.api_key)
            self.layout.addRow(_meta.name, widget)
            return widget

        for attribute, meta in attributes:
            if meta.hidden:
                continue
            self._data_widgets[attribute] = add_attribute(attribute, meta, backend)

    def _load_backend_values(self, backend: bi.BackendConfig) -> None:
        """
        Load the values of the backend settings.
        """

        attributes: list[tuple[str, bi.AttributeMetadata]] = list(
            backend.attribute_metadata().items()
        )

        for attribute, meta in attributes:
            if meta.hidden:
                continue
            self._data_widgets[attribute].set_value(getattr(backend, attribute))

    def read_values(self) -> bi.BackendConfig:
        """
        Update the values of the backend settings based on widget values.

        :returns: The backend config with the updated values.
        """
        if self.current_backend is None:
            raise ValueError("No backend loaded")

        for attribute, widget in self._data_widgets.items():
            setattr(self.current_backend, attribute, widget.get_value())

        return self.current_backend
