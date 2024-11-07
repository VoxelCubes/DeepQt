"""
This is the generic interface for reliable and unreliable backends.
As a baseclass, it dictates the public methods of a backend,
to make dependency inversion and injection possible.

Reliable backends are expected to translate the text consistently and correctly.
    e.g. DeepL
Unreliable backends may return nonsense and need per segment tweaking to work.
    e.g. ChatGPT, LLMs in general.
"""

from abc import abstractmethod, ABC
from enum import StrEnum, auto, Enum
from pathlib import Path
from typing import Protocol, final, NewType

import PySide6.QtGui as Qg
from attrs import frozen, define

import deepqt.constants as ct
import deepqt.gui_utils as gu

# This is some unique identifier for the backend,
# since multiple may be of the same type.
BackendID = NewType("BackendId", str)
BackendIdNone = BackendID("")


# Any backend's translation functions can only raise these two exceptions.
class TranslationFailed(Exception):
    """
    Raised when a translation fails for any reason.
    """

    pass


class UnsupportedFileFormat(Exception):
    """
    Raised when a file format is not supported by the backend.
    """

    pass


class TranslationAborted(Exception):
    """
    Raised when a translation is aborted by the user.
    """

    pass


@frozen
class ConfigIssue:
    """
    When checking each attribute of a BackendConfig, we need to know the name of the
    attribute, what the problem is, and if this is a critical issue so that it can be
    more prominently displayed in the gui.
    """

    attribute: str
    message: str
    critical: bool


class BackendIconType(StrEnum):
    """
    This defines the available namespaces for backend icons.
    Custom: Icons supplied by DeepQt.
    XDG: Icons supplied by the system.
    User: Icons supplied by the user, e.g. a custom path.
    """

    CUSTOM = "custom/"
    XDG = "xdg/"
    USER = "user/"

    def __truediv__(self, other: str):
        """
        Concatenate the icon type with a string. This serves to show that this
        enum is a namespace for icons.
        """
        return self.value + other


@define
class AttributeMetadata:
    """
    Metadata for an attribute.

    hidden means the value is not configurable by the user.
    no_save means the value is not saved to or read from the config file.
    """

    name: str = ""
    type: type = None
    description: str = ""
    hidden: bool = None  # Defaults to True if no_save is True, otherwise False.
    no_save: bool = False

    def __attrs_post_init__(self):
        if self.hidden is None:
            self.hidden = self.no_save


class ConnectionStatus(Enum):
    Connected = auto()
    Offline = auto()
    Error = auto()


@frozen
class BackendStatus:
    """
    Status information specific to the backend.
    E.g. remaining characters, connection good/bad etc.
    A count of None means to hide usage because it's not applicable.
    A limit of None means unlimited usage.
    """

    connection: ConnectionStatus = ConnectionStatus.Offline
    usage_count: int | None = None
    usage_limit: int | None = None


@define
class BackendConfig(ABC):
    # How long it took to translate 1000 characters on average. (-1 if unknown)
    backend_type: ct.Backend = None  # Needed to parse the config.
    name: str = "Unset"
    icon: str = BackendIconType.CUSTOM / "generic-backend.svg"
    description: str = "Blank description."  # Markdown enabled.
    unreliable: bool = False
    help: ct.HTML = ""
    paid: bool = False
    avg_time_per_mille: float = -1.0

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> "BackendConfig": ...

    @abstractmethod
    def validate(self) -> list[ConfigIssue]:
        """
        Returns a list of error messages if the config is invalid.
        Meaning that an empty list as a return value implies the config is valid.
        """
        ...

    @abstractmethod
    def _attribute_metadata(self) -> dict[str, AttributeMetadata]:
        """
        Internal method to define the metadata for each attribute.
        This one is to be overridden by the implementing class.
        """
        ...

    @final
    def attribute_metadata(self) -> dict[str, AttributeMetadata]:
        """
        Returns the metadata for each attribute.
        Hidden metadata won't be configurable by the user.
        No-save metadata won't be saved to the config file and is automatically hidden.
        """
        # Validate each attribute in the class is covered.
        meta = {
            "backend_type": AttributeMetadata(
                type=ct.Backend,
                hidden=True,
            ),
            "name": AttributeMetadata(
                type=str,
                hidden=True,  # Name is displayed in the header, so hide it from the list.
            ),
            "icon": AttributeMetadata(
                type=str,
                no_save=True,
            ),
            "description": AttributeMetadata(
                type=str,
                no_save=True,
            ),
            "unreliable": AttributeMetadata(
                type=bool,
                no_save=True,
            ),
            "help": AttributeMetadata(
                type=ct.HTML,
                no_save=True,
            ),
            "paid": AttributeMetadata(
                type=bool,
                no_save=True,
            ),
            "avg_time_per_mille": AttributeMetadata(
                # Historical average time to translate 1000 characters, internal use only.
                type=float,
                hidden=True,
            ),
        }
        # Append the child metadata.
        child_meta = self._attribute_metadata()
        meta.update(child_meta)
        return meta

    def load_icon(self) -> Qg.QIcon:
        """
        Load the icon from the icon path, depending on the namespace.
        If a USER icon fails to load, it will return a placeholder.
        """
        if self.icon.startswith(BackendIconType.CUSTOM):
            custom_icon_name = self.icon.removeprefix(BackendIconType.CUSTOM)
            return gu.load_custom_icon(custom_icon_name)
        elif self.icon.startswith(BackendIconType.XDG):
            return Qg.QIcon.fromTheme(self.icon.removeprefix(BackendIconType.XDG))
        elif self.icon.startswith(BackendIconType.USER):
            icon = Qg.QIcon(self.icon.removeprefix(BackendIconType.USER))
            if icon.isNull():
                return Qg.QIcon.fromTheme("image-missing")
        else:
            raise ValueError(f"Invalid icon type: {self.icon}")

    def no_save_attributes(self) -> list[str]:
        """
        Returns a list of attribute names that should not be saved to the config file.
        This is because the name, description etc. should be defined in the code, without the possibility
        of stale names and descriptions being stuck in the config file, never getting updated.
        """
        return [key for key, meta in self.attribute_metadata().items() if meta.no_save]


class Backend(ABC):
    """
    This class defines the working interface for a backend,
    managing the connection and api calls.
    This is composed with a BackendConfig object to store the settings.
    """

    _config: BackendConfig | None  # Needs to be passed from the config.

    def __init__(self) -> None:
        self._config = None

    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def disconnect(self) -> None: ...

    @abstractmethod
    def supported_languages(self) -> list[tuple[str, str]]:
        """
        Returns a list of supported languages in the form of tuples (code, name).
        Example: [('en', 'English'), ('de', 'German'), ...]
        """
        ...

    @abstractmethod
    def supported_formats(self) -> list[ct.Formats]:
        """
        These are the supported file formats: Text, Epub, PDF etc.
        """
        ...

    @abstractmethod
    def config(self) -> BackendConfig: ...

    @abstractmethod
    def default_config(self) -> BackendConfig: ...

    @abstractmethod
    def set_config(self, config: BackendConfig) -> None: ...

    @abstractmethod
    def translate_text(self, text: str) -> str: ...

    @abstractmethod
    def translate_file(self, file_in: Path, file_type: ct.Formats, file_out: Path) -> None: ...

    @abstractmethod
    def status(self) -> BackendStatus:
        """
        Contains status information specific to the backend.
        E.g. remaining characters, connection good/bad etc.
        """
        ...


class ReliableBackend(Backend, ABC): ...


class UnreliableBackend(Backend, ABC): ...
