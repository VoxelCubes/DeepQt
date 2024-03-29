"""
This is the generic interface for reliable and unreliable backends.
As a protocol, it dictates the public methods of a backend,
to make dependency inversion and injection possible.

Reliable backends are expected to translate the text consistently and correctly.
    e.g. DeepL
Unreliable backends may return nonsense and need per segment tweaking to work.
    e.g. ChatGPT, LLMs in general.
"""

from abc import abstractmethod, ABC
from pathlib import Path
from typing import Protocol, final

from attrs import frozen, define

import deepqt.constants as ct


# Any backend's translation functions can only raise these two exceptions.
class TranslationFailed(Exception):
    """
    Raised when a translation fails for any reason.
    """

    ...


class TranslationAborted(Exception):
    """
    Raised when a translation is aborted by the user.
    """

    ...


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


@frozen
class AttributeMetadata:
    """
    Metadata for an attribute.
    """

    name: str
    type: type
    description: str
    hidden: bool = False


@frozen
class BackendStatus:
    """
    Status information specific to the backend.
    E.g. remaining characters, connection good/bad etc.
    """

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
        """
        # Validate each attribute in the class is covered.
        meta = self._attribute_metadata()
        # Add whatever is missing from this base class.
        return meta


@define
class BackendConfig(ABC):
    # How long it took to translate 1000 characters on average. (-1 if unknown)
    avg_time_per_mille: float = -1.0

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> "BackendConfig":
        ...

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
        """
        # Validate each attribute in the class is covered.
        meta = {
            "avg_time_per_mille": AttributeMetadata(
                name="Average time per 1000 characters",
                type=float,
                description="Historical average time to translate 1000 characters, internal use only.",
                hidden=True,
            )
        }
        # Append the child metadata.
        child_meta = self._attribute_metadata()
        meta.update(child_meta)
        return meta


class Backend(Protocol):
    def connect(self) -> None:
        ...

    def disconnect(self) -> None:
        ...

    def supported_languages(self) -> list[tuple[str, str]]:
        """
        Returns a list of supported languages in the form of tuples (code, name).
        Example: [('en', 'English'), ('de', 'German'), ...]
        """
        ...

    def supported_formats(self) -> list[ct.Formats]:
        """
        These are the supported file formats: Text, Epub, PDF etc.
        """
        ...

    def config(self) -> BackendConfig:
        ...

    def default_config(self) -> BackendConfig:
        ...

    def set_config(self, config: BackendConfig) -> None:
        ...

    def translate_text(self, text: str) -> str:
        ...

    def translate_file(self, file_in: Path, file_out: Path) -> None:
        ...

    def status(self) -> BackendStatus:
        """
        Contains status information specific to the backend.
        E.g. remaining characters, connection good/bad etc.
        """
        ...


class ReliableBackend(Backend):
    ...


class UnreliableBackend(Backend):
    ...
