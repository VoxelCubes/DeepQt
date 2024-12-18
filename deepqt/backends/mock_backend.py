from itertools import cycle
from io import StringIO
from itertools import cycle
from pathlib import Path

from attrs import define

import deepqt.backends.backend_interface as bi
import deepqt.constants as ct
import deepqt.utils as ut


# Note: dataclass attributes MUST have a type annotation, otherwise they won't be loaded from the subclass.
@define
class MockConfig(bi.BackendConfig):
    backend_type: ct.Backend = ct.Backend.MOCK
    name: str = "Mock"
    description: str = (
        'This is a "fake" backend for **testing purposes**.\n '
        "It simulates a reliable translation service, "
        "meaning one that is expected to always return a translation, without much (if any) supervision.\n"
        "This is as opposed to LLM chatbots that may return nonsense at a high rate, "
        "if not outright refuse to perform the task asked of them."
    )
    unreliable = True
    chunk_size: int = 1000
    wait_time: ct.Milliseconds = 1000

    @classmethod
    def from_dict(cls, data: dict) -> tuple["MockConfig", list[Exception]]:
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
            "chunk_size": bi.AttributeMetadata(
                name="Chunk size",
                type=int,
                description="Number of characters to translate at once.",
            ),
            "wait_time": bi.AttributeMetadata(
                name="Wait time",
                type=ct.Milliseconds,
                description="Time to wait between chunks (ms).",
            ),
        }


class MockBackend(bi.ReliableBackend):
    """
    Backend for debugging.
    """

    _config: MockConfig | None  # Needs to be passed from the config.
    _connection: bi.ConnectionStatus

    def __init__(self) -> None:
        super().__init__()
        self._status = bi.ConnectionStatus.Offline

    def connect(self) -> None:
        # No connection needed.
        self._status = bi.ConnectionStatus.Connected

    def disconnect(self) -> None:
        # Nothing to disconnect.
        self._status = bi.ConnectionStatus.Offline
        pass

    def supported_languages(self) -> list[tuple[str, str]]:
        """
        Returns a list of supported languages in the form of tuples (code, name).
        Example: [('en', 'English'), ('de', 'German'), ...]
        """
        return [("en", "English"), ("ent", "Englishn't")]

    def supported_formats(self) -> list[ct.Formats]:
        """
        These are the supported file formats: Text, Epub, PDF etc.
        """
        return [ct.Formats.TEXT]

    def config(self) -> MockConfig:
        return self._config

    def default_config(self) -> MockConfig:
        return MockConfig()

    def set_config(self, config: MockConfig) -> None:
        self._config = config

    def translate_text(self, text: str) -> str:
        """
        Replaces all alphabetical characters with "translated", preserving the case.
        """
        translation = cycle("translated")
        buffer = StringIO()
        for char in text:
            if char.isalpha():
                if char.isupper():
                    buffer.write(next(translation).upper())
                else:
                    buffer.write(next(translation))
            else:
                buffer.write(char)
        return buffer.getvalue()

    def translate_file(self, file_in: Path, file_type: ct.Formats, file_out: Path) -> None:
        if file_type is ct.Formats.TEXT:
            try:
                with ut.read_autodetect_encoding(file_in) as f:
                    text = f.read()
                translated = self.translate_text(text)
                file_out.write_text(translated)
            except Exception as e:
                raise bi.TranslationFailed(f"Error translating file: {e}")
        else:
            raise bi.UnsupportedFileFormat(f"Unsupported file format: {file_type}")

    def status(self) -> bi.BackendStatus:
        """
        Contains status information specific to the backend.
        E.g. remaining characters, connection good/bad etc.
        """
        return bi.BackendStatus(self._status, None, None)
