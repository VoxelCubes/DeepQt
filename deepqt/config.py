import json
import shutil
from pathlib import Path

import attrs
import yaml
from attrs import define, Factory
from cattrs import Converter
from loguru import logger

import deepqt.backends.backend_interface as bi
import deepqt.backends.deepl_backend as db
import deepqt.backends.mock_backend as mb
import deepqt.constants as ct
import deepqt.utils as ut


backend_to_config = {
    ct.Backend.MOCK: mb.MockConfig,
    ct.Backend.DEEPL: db.DeepLConfig,
}


@define
class Config:
    lang_from: str = ""
    lang_to: str = ""

    use_fixed_output_path: bool = False
    fixed_output_path: str = ""

    glossary_path: str = ""
    use_glossary: bool = True

    # Advanced options not shown on the mainwindow:
    dump_on_abort: bool = True
    epub_nuke_kobo: bool = True
    epub_nuke_ruby: bool = True
    epub_nuke_indents: bool = True
    epub_crush: bool = False
    epub_make_text_horizontal: bool = True
    epub_ignore_empty_html: bool = True

    # Backend configs:
    last_backend: ct.Backend = ct.Backend.DEEPL
    backend_configs: dict[ct.Backend, bi.BackendConfig] = Factory(dict)

    def __attrs_post_init__(self):
        # Preload the backend configs.
        self.backend_configs = {backend: conf_class() for backend, conf_class in backend_to_config.items()}

    def save(self, path: Path = None) -> bool:
        """
        Write to a temporary file and then move it to the destination.
        If the write fails, the temporary file is deleted.
        When the path is None, the config is saved to the default location.

        :param path: [Optional] The path to write the profile to.
        :return: True if the profile was written successfully, False otherwise.
        """

        if path is None:
            path = ut.get_config_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = path.with_suffix(".tmp")
        converter = config_converter_factory()
        success = self._unsafe_save(temp_path, converter)
        if success:
            try:
                shutil.move(temp_path, path)
            except Exception:
                logger.exception(f"Failed to rename {temp_path} to {path}")
                success = False
        if not success:
            try:
                if temp_path.exists():
                    temp_path.unlink()
            except Exception:
                logger.exception(f"Failed to delete {temp_path}")
        return success

    def _unsafe_save(self, path: Path, converter: Converter) -> bool:
        """
        Write the config to a file.

        :param path: The path to write the config to.
        :param converter: The cattrs converter to use.
        :return: True if the config was written successfully, False otherwise.
        """
        logger.debug("Writing config to disk...")
        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(converter.unstructure(self), file, indent=4)
            return True
        except Exception:
            logger.exception(f"Failed to write profile to {path}")
            return False

    def safe_dump(self) -> dict:
        """
        Dump the config to a dictionary, but do not include the backend configs.
        """
        converter = config_converter_factory()

        # Censor all attributes that have the suffix "_key".
        def censor_keys_hook(inst):
            result = {}
            for field in attrs.fields(inst.__class__):
                value = getattr(inst, field.name)
                if field.name.endswith("_key"):
                    value = ut.censor_key(value)
                if attrs.has(value):
                    # If the value is also an attrs class, unstructure it recursively
                    value = converter.unstructure(value)
                result[field.name] = value
            return result

        converter.register_unstructure_hook(bi.BackendConfig, censor_keys_hook)

        # Using yaml safe dump to avoid having any object constructors in the output.
        # Convert all Backend string enums to their base string, so safe_dump can handle them.

        # Using the name instead of the value because I think the upper case looks nicer.
        converter.register_unstructure_hook(ct.Backend, lambda x: x.name)

        data = converter.unstructure(self)
        return data

    def pretty_log(self) -> None:
        """
        Log the config in a safe, easily readable format to debug.
        """
        data = self.safe_dump()
        # Dump to yaml string.
        logger.debug(yaml.safe_dump(data, default_flow_style=False, sort_keys=False))


def load_config(conf_path: Path) -> tuple[Config, bool, list[Exception]]:
    """
    Load the configuration from the given path.
    If no errors occur, return the config, True, and an empty list.
    If a critical error occurs, return the config, False, and the error.
    If non-critical errors occur, return the config, True, and the errors.

    :param conf_path: Path to the configuration file.
    :return: The configuration, whether it was loaded successfully (fully or in part), and any errors.
    """

    config = Config()

    success = True
    errors: list[Exception]

    try:
        with open(conf_path, "r") as f:
            # Load the default config, then update it with the values from the config file.
            # This way, missing values will be filled in with the default values.
            json_data = json.load(f)

            errors = ut.load_dict_to_attrs_safely(config, json_data, skip_attrs=["backend_configs"])

            if "backend_configs" in json_data:
                # Attempt to structure the json data into the correct backend config class,
                # based on the backend name.
                backend_configs, backend_errors = structure_backend_configs(json_data["backend_configs"])
                config.backend_configs.update(backend_configs)
                errors.extend(backend_errors)
    except OSError as e:
        logger.exception(f"Failed to read config file {conf_path}")
        errors = [type(e)(f"Failed to read config file {conf_path}: {e}")]
        success = False
    except (KeyError, TypeError, json.decoder.JSONDecodeError) as e:
        logger.exception(f"Configuration file could not be parsed {conf_path}")
        errors = [type(e)(f"Configuration file could not be parsed {conf_path}: {e}")]
        success = False

    # If fubar, reset the config just to be sure.
    if not success:
        config = Config()

    return config, success, errors


class UnknownBackend(Exception):
    pass


def structure_backend_configs(json_data: dict[str, dict]) -> tuple[dict[ct.Backend, bi.BackendConfig], list[Exception]]:
    """
    Attempt to structure the json data into the correct backend config class,
    based on the backend name.

    If the error list is empty, no exceptions occurred.

    :param json_data: The json data to structure.
    :return: The structured backend configs and any errors that occurred.
    """
    errors: list[Exception] = []
    json_keys = list(json_data.keys())
    backend_data: dict[ct.Backend, bi.BackendConfig | dict] = {}

    # Cast the key strings to the Backend enum.
    for backend_name in json_keys:
        try:
            backend_enum = ct.Backend(backend_name)
            backend_data[backend_enum] = json_data[backend_name]
        except ValueError:
            logger.error(f"Unknown backend: {backend_name}")
            errors.append(UnknownBackend(backend_name))

    for backend in backend_data:
        # Because the string and the strenum hashes are identical and Python treats them as equal,
        # we can simply ask the json_data using the strenum as a key as well.
        # Alternatively, to be fully correct, use backend.value but the static type checker
        # didn't like it for some reason, at least not a valid one.
        try:
            if backend == ct.Backend.MOCK:
                backend_data[backend], backend_errors = mb.MockConfig.from_dict(json_data[backend])
            elif backend == ct.Backend.DEEPL:
                backend_data[backend], backend_errors = db.DeepLConfig.from_dict(json_data[backend])
            else:
                logger.error(f"Unknown backend: {backend}")
                backend_errors = [UnknownBackend(f"Unknown backend: {backend}")]

            errors.extend(backend_errors)

        except Exception as e:
            logger.exception(f"Failed to structure backend config for {backend}")
            errors.append(type(e)(f"Failed to structure backend config for {backend}: {e}"))

    return backend_data, errors


def config_converter_factory() -> Converter:
    """
    Create a cattrs converter with the necessary overrides for the Config class.

    This is only used when unstructuring, as cattrs isn't fault tolerant enough when
    structuring and doesn't provide errors either.
    """
    converter = Converter()
    converter.register_unstructure_hook(bi.BackendConfig, attrs.asdict)
    return converter
