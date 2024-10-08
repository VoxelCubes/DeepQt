from pathlib import Path
from typing import Any

from attrs import define
import deepl

import deepqt.backends.backend_interface as bi
import deepqt.constants as ct
import deepqt.utils as ut

# This is the value returned by the API if the user has unlimited usage.
DEEPL_USAGE_UNLIMITED = 1_000_000_000_000


@define
class DeepLConfig(bi.BackendConfig):
    backend_type: ct.Backend = ct.Backend.DEEPL
    name: str = "DeepL"
    icon: str = bi.BackendIconType.CUSTOM / "deepl.png"
    description: str = (
        "DeepL is a high-quality translation service that uses neural networks to translate text."
    )
    unreliable: bool = True
    paid: bool = True
    api_key: ct.APIKey = ct.APIKey("sdkfjhasdflasjfhjsalhfla")
    tl_max_chunks: int = 20
    tl_min_chunk_size: int = 5_000
    tl_preserve_formatting: bool = True
    wait_time: ct.Milliseconds = 1000
    help: ct.HTML = """<html> <head/> <body>
        <p> To use this specific translation service you need a DeepL API key.
            You can get one by signing up for an account at 
            <a href="https://www.deepl.com/pro-api">deepl.com</a>.
        </p>
        <p> For more information on the API, see the 
            <a href="https://github.com/VoxelCubes/DeepQt/blob/master/docs/api_help.md">
            online documentation</a>.
        </p> </body> </html>"""

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
                type=ct.APIKey,
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


class DeepLBackend(bi.ReliableBackend):
    """
    Backend for DeepL.
    """

    _config: DeepLConfig | None  # Needs to be passed from the config.
    _connection: bi.ConnectionStatus

    def __init__(self) -> None:
        super().__init__()
        self._status = bi.ConnectionStatus.Offline

    def connect(self) -> None: ...

    def disconnect(self) -> None: ...

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

    def config(self) -> dict[str, Any]: ...

    def default_config(self) -> dict[str, Any]: ...

    def set_config(self, config: dict[str, Any]) -> None: ...

    def translate_text(self, text: str) -> str: ...

    def translate_file(self, file_in: Path, file_type: ct.Formats, file_out: Path) -> None: ...

    def status(self) -> bi.BackendStatus:
        """
        Contains status information specific to the backend.
        E.g. remaining characters, connection good/bad etc.
        """
        return bi.BackendStatus()
