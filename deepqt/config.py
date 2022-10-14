import json
import os
import platform
from dataclasses import dataclass, asdict
from pathlib import Path

from logzero import logger

from deepqt import __program__, helpers as hp


@dataclass
class Config:
    lang_from: str
    lang_to: str

    use_fixed_output_path: bool
    fixed_output_path: str

    glossary_path: str
    use_glossary: bool
    use_quote_protection: bool

    api_key: str

    # Advanced options.
    tl_max_chunks: int
    tl_min_chunk_size: int
    tl_preserve_formatting: bool
    tl_mock: bool
    dump_on_abort: bool
    epub_nuke_kobo: bool
    epub_nuke_ruby: bool
    epub_nuke_indents: bool
    epub_crush: bool
    epub_make_text_horizontal: bool
    epub_ignore_empty_html: bool
    # Timing history.
    avg_time_per_mille: float

    def save(self):
        conf_path = config_path()
        try:
            with open(conf_path, "w") as f:
                json.dump(asdict(self), f, indent=4)
                logger.debug("Saved config")
        except OSError as e:
            hp.show_critical(
                None,
                "Failed to write file",
                f'Failed to write config file "{conf_path}"\n\n{e}',
            )

    @classmethod
    def load(cls) -> "Config":
        ensure_config_exists()

        conf_path = config_path()

        if not os.path.exists(conf_path.parent):
            os.makedirs(conf_path.parent)

        try:
            with open(conf_path, "r") as f:
                # Load the default config, then update it with the values from the config file.
                # This way, missing values will be filled in with the default values.
                conf = cls(**asdict(default_config()))
                conf.__dict__.update(json.load(f))
                return conf
        except OSError as e:
            error_message = f'Failed to read config file "{conf_path}"\n\n{e}'
        except (KeyError, TypeError, json.decoder.JSONDecodeError) as e:
            error_message = f'Configuration file malformed "{conf_path}"\n\n{e}'

        conf = default_config()
        if hp.show_question(
            None,
            "Failed to read file",
            f"{error_message}\n\nDo you want to reset the config file? "
            "(Cancel to proceed with default config, but will overwrite the existing file if "
            "settings are changed from within this program.",
        ):
            conf.save()

        return conf

    def safe_dump(self) -> str:
        """
        Dump the config to a dict and obfuscate the api key to prevent it from leaking into logs.

        :return: Stringified dictionary.
        """

        conf = asdict(self)
        conf["api_key"] = "".join(["X" if char.isalnum() else char for char in conf["api_key"]])
        return str(conf)


def config_path() -> Path:
    """
    Get the path to the configuration file for both Linux and Windows.
    """
    if platform.system() == "Linux":
        from xdg import XDG_CONFIG_HOME

        return Path(XDG_CONFIG_HOME, __program__.lower() + "rc")
    elif platform.system() == "Windows":
        return Path(os.getenv("APPDATA"), __program__.lower(), "config.ini")
    else:  # ???
        raise NotImplementedError("Your OS is currently not supported.")


def cache_path() -> Path:
    """
    Get the path to the cache directory.
    """
    if platform.system() == "Linux":
        from xdg import XDG_CACHE_HOME

        return Path(XDG_CACHE_HOME, __program__.lower())
    elif platform.system() == "Windows":
        return Path(os.getenv("APPDATA"), __program__.lower())
    else:  # ???
        raise NotImplementedError("Your OS is currently not supported.")


def epub_cache_path(epub_path: None | Path = None) -> Path:
    """
    Get the path to the epub cache directory for this epub.
    Each epub gets its own cache directory, to keep them separate.

    :param epub_path: (Optional) Path to the epub file. If None, return the cache directory.
    :return: Path to the cache directory.
    """
    if epub_path is None:
        return cache_path() / "epubs"
    return cache_path() / "epubs" / epub_path.name


def log_path() -> Path:
    """
    Get the path to the log file.
    Use the cache directory for this.
    """
    return cache_path() / f"{__program__.lower()}.log"


def default_config() -> Config:
    """
    Get the default config.
    """
    return Config(
        lang_from="",
        lang_to="",
        use_fixed_output_path=False,
        fixed_output_path="",
        glossary_path="",
        use_glossary=True,
        use_quote_protection=True,
        api_key="",
        tl_max_chunks=20,
        tl_min_chunk_size=10_000,
        tl_preserve_formatting=True,
        tl_mock=False,
        dump_on_abort=True,
        epub_nuke_kobo=True,
        epub_nuke_ruby=True,
        epub_nuke_indents=True,
        epub_make_text_horizontal=True,
        epub_crush=False,  # This could confuse deepl and subsequent epub readers too much.
        epub_ignore_empty_html=True,
        avg_time_per_mille=0.33,  # This was measured experimentally. Depends on local internet connection.
    )


def ensure_config_exists():
    """
    Ensure that the config file exists.
    If it does not exist, create the default config file.
    """
    conf_path = config_path()
    if not conf_path.is_file():
        logger.warning(f'Config file "{conf_path}" not found. Creating default config file.')
        default_config().save()
