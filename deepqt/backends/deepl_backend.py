from pathlib import Path
from typing import Any

from attrs import define
import deepl

import deepqt.backends.backend_interface as bi
import deepqt.constants as ct
import deepqt.utils as ut

DEEPL_USAGE_UNLIMITED = 1_000_000_000_000  # This is the value returned by the API if the user has unlimited usage.


@define
class DeepLConfig(bi.BackendConfig):
    name: str = "DeepL"
    api_key: ct.APIKey = "sdkfjhasdflasjfhjsalhfla"
    tl_max_chunks: int = 20
    tl_min_chunk_size: int = 5_000
    tl_preserve_formatting: bool = True
    wait_time: ct.Milliseconds = 1000

    @classmethod
    def from_dict(cls, data: dict) -> tuple["DeepLConfig", list[Exception]]:
        dataclass = cls()
        no_save_attrs = dataclass.no_save_attributes()
        return dataclass, ut.load_dict_to_attrs_safely(
            dataclass, data, skip_attrs=no_save_attrs, include_until_base=bi.BackendConfig
        )

    def validate(self) -> list[bi.ConfigIssue]:
        """
        Returns a list of error messages if the config is invalid.
        Meaning that an empty list as a return value implies the config is valid.
        """
        return []

    def _attribute_metadata(self) -> dict[str, bi.AttributeMetadata]:
        return {
            "api_key": bi.AttributeMetadata(
                name="API key",
                type=str,
                description="DeepL API key.",
            ),
            "tl_max_chunks": bi.AttributeMetadata(
                name="Max chunks",
                type=int,
                description="Maximum number of chunks to split the text into.",
            ),
            "tl_min_chunk_size": bi.AttributeMetadata(
                name="Min chunk size",
                type=int,
                description="Minimum number of characters per chunk.",
            ),
            "tl_preserve_formatting": bi.AttributeMetadata(
                name="Preserve formatting",
                type=bool,
                description="Preserve formatting in the translated text.",
            ),
            "wait_time": bi.AttributeMetadata(
                name="Wait time",
                type=ct.Milliseconds,
                description="Time to wait between chunks (ms).",
            ),
        }


@define
class DeepLStatus(bi.BackendStatus):
    ready: bool = True

    def _attribute_metadata(self) -> dict[str, bi.AttributeMetadata]:
        return {
            "ready": bi.AttributeMetadata(
                name="Ready",
                type=bool,
                description="Whether the backend is ready to translate.",
            )
        }


class DeepLBackend(bi.ReliableBackend):
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

    def config(self) -> dict[str, Any]:
        ...

    def default_config(self) -> dict[str, Any]:
        ...

    def set_config(self, config: dict[str, Any]) -> None:
        ...

    def translate_text(self, text: str) -> str:
        ...

    def translate_file(self, file_in: Path, file_out: Path) -> None:
        ...

    def status(self) -> dict[str, Any]:
        """
        Contains status information specific to the backend.
        E.g. remaining characters, connection good/bad etc.
        """
        ...
