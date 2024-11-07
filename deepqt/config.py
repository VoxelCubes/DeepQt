import json
import shutil
from pathlib import Path
from typing import Callable, Any, NewType

import attrs
import yaml
from attrs import define, Factory
from cattrs import Converter
from loguru import logger
from collections import namedtuple

import deepqt.backends.backend_interface as bi
import deepqt.backends.lookups as b_lut  # backend lookup table
import deepqt.constants as ct
import deepqt.utils as ut


@define
class Config:
    gui_theme: str = ""  # Blank means system theme.

    lang_from: str = ""
    lang_to: str = ""

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
    current_backend: bi.BackendID = bi.BackendIdNone
    backend_configs: dict[bi.BackendID, bi.BackendConfig] = Factory(dict)

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
        success = self._unsafe_save(temp_path)
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

    def _unsafe_save(self, path: Path) -> bool:
        """
        Write the config to a file.

        :param path: The path to write the config to.
        :return: True if the config was written successfully, False otherwise.
        """
        logger.debug("Writing config to disk...")
        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(self.dump(), file, indent=4)
            return True
        except Exception:
            logger.exception(f"Failed to write profile to {path}")
            return False

    def dump(self, converter: Converter = None) -> dict:
        """
        Dump the config to a dictionary.
        """
        if converter is None:
            converter = config_converter_factory()

        data = converter.unstructure(self)

        # Check for any backend attributes that have the "no_save" metadata flag set.
        # We must exclude these from the dump.
        # Using cattrs's omit doesn't work because as far as it's concerned, all backends
        # are of type BackendConfig, but not all of the actual subclasses have the same attributes,
        # which causes an attribute error for whatever reason.

        for backend_id, backend_config in self.backend_configs.items():
            no_save_attrs = backend_config.no_save_attributes()
            for attr_name in no_save_attrs:
                del data["backend_configs"][backend_id][attr_name]
        return data

    def safe_dump(self) -> dict:
        """
        Dump the config to a dictionary, but censor api keys.
        This is dumped to the log, which users are encouraged to share when debugging.
        """
        converter = config_converter_factory()

        # Censor all attributes that have the suffix "_key".
        def censor_keys_hook(inst) -> dict:
            result = {}
            for field in attrs.fields(inst.__class__):
                value = getattr(inst, field.name)
                if field.name.endswith("_key"):
                    value = ut.censor_key(value)
                if attrs.has(value):
                    # If the value is also an attrs class, unstructure it recursively
                    value = censor_keys_hook(value)
                else:
                    value = converter.unstructure(value)
                result[field.name] = value
            return result

        converter.register_unstructure_hook(bi.BackendConfig, censor_keys_hook)

        # Using yaml safe dump to avoid having any object constructors in the output.
        # Convert all Backend string enums to their base string, so safe_dump can handle them.

        converter.register_unstructure_hook(ct.Backend, lambda x: x.value)

        data = converter.unstructure(self)

        # Do the same cleanup as in dump()
        for backend_id, backend_config in self.backend_configs.items():
            no_save_attrs = backend_config.no_save_attributes()
            for attr_name in no_save_attrs:
                del data["backend_configs"][backend_id][attr_name]
        return data

    def pretty_log(self) -> None:
        """
        Log the config in a safe, easily readable format to debug.
        """
        data = self.safe_dump()
        # Dump to yaml string.
        logger.debug("Config:\n" + yaml.safe_dump(data, default_flow_style=False, sort_keys=False))


def load_config(conf_path: Path, config_factory: Callable[[], Any] = Config) -> tuple[
    Config,
    list[ut.RecoverableParseException],
    list[ut.ParseError],
    list[ut.CriticalParseError],
]:
    """
    Load the configuration from the given path.
    If any errors occur, they will be returned as Exception objects in the corresponding
    severity list.

    :param conf_path: Path to the configuration file.
    :param config_factory: [Optional] Factory function to create a new config object.
    :return: The configuration and 3 lists of errors.
    """

    config = config_factory()

    recoverable_exceptions: list[ut.RecoverableParseException] = []
    errors: list[ut.ParseError] = []
    critical_errors: list[ut.CriticalParseError] = []

    try:
        with open(conf_path, "r") as f:
            # Load the default config, then update it with the values from the config file.
            # This way, missing values will be filled in with the default values.
            json_data = json.load(f)

            recoverable_exceptions = ut.load_dict_to_attrs_safely(
                config, json_data, skip_attrs=["backend_configs"]
            )

            if "backend_configs" in json_data:
                # Attempt to structure the json data into the correct backend config class,
                # based on the backend type.
                backend_configs, backend_recoverable_exceptions, backend_errors = (
                    structure_backend_configs(json_data["backend_configs"])
                )
                config.backend_configs.update(backend_configs)
                recoverable_exceptions.extend(backend_recoverable_exceptions)
                errors.extend(backend_errors)
    except OSError as e:
        logger.exception(f"Failed to read config file {conf_path}")
        critical_errors = [
            ut.CriticalParseError(
                f"{type(e).__name__}: Failed to read config file {conf_path}: {e}"
            )
        ]
    except json.decoder.JSONDecodeError as e:
        logger.exception(f"Configuration file could not be parsed {conf_path}")
        critical_errors = [
            ut.CriticalParseError(
                f"{type(e).__name__}: Configuration file could not be parsed {conf_path}: {e}"
            )
        ]

    # If's fubar, reset the config just to be sure.
    if critical_errors:
        config = config_factory()

    return config, recoverable_exceptions, errors, critical_errors


def structure_backend_configs(
    json_data: dict[str, dict]
) -> tuple[
    dict[bi.BackendID, bi.BackendConfig], list[ut.RecoverableParseException], list[ut.ParseError]
]:
    """
    Attempt to structure the json data into the correct backend config class,
    based on the backend type in the id.

    If the error lists are empty, no errors occurred.

    :param json_data: The json data to structure.
    :return: The structured backend configs and any recoverable and non-recoverable errors.
    """
    recoverable_exceptions: list[ut.RecoverableParseException] = []
    errors: list[ut.ParseError] = []
    json_keys = list(json_data.keys())
    backend_data: dict[bi.BackendID, bi.BackendConfig | dict] = {}
    corrupted_backends: list[bi.BackendID] = []

    # Cast the key ints to the BackendID type.
    # It honestly doesn't matter what type they are, as long as they're hashable,
    # which they are, coming from json.
    for backend_id in json_keys:
        backend_data[bi.BackendID(backend_id)] = json_data[backend_id]

    for backend_id in backend_data:
        try:
            # Look into the backend_type field to determine the backend type.
            backend_type_raw = str(json_data[backend_id]["backend_type"]).upper()
            backend_type = ct.Backend(backend_type_raw)
        except KeyError:
            logger.error(f'Backend "{backend_id}" has no backend_type field')
            errors.append(
                ut.ParseError(
                    f'Backend "{backend_id}" has no backend_type field. The backend could not be loaded!'
                )
            )
            # Purge this backend from the data.
            corrupted_backends.append(backend_id)
            continue
        except ValueError:
            backend_type_raw = str(json_data[backend_id]["backend_type"])
            logger.error(f'Unknown backend type: "{backend_type_raw}" for backend "{backend_id}"')
            errors.append(
                ut.ParseError(
                    f'Unknown backend type: "{backend_type_raw}" for backend "{backend_id}"'
                )
            )
            # Purge this backend from the data.
            corrupted_backends.append(backend_id)
            continue

        # Because the string and the strenum hashes are identical and Python treats them as equal,
        # we can simply ask the json_data using the strenum as a key as well.
        # Alternatively, to be fully correct, use backend.value but the static type checker
        # didn't like it for some reason, likely a false positive.
        try:
            config_obj = b_lut.backend_to_config[backend_type]
            backend_data[backend_id], backend_exceptions = config_obj.from_dict(
                backend_data[backend_id]
            )
            # Prepend the backend id to the error messages.
            backend_exceptions = [
                ut.RecoverableParseException(f'Backend "{backend_id}": {str(e)}')
                for e in backend_exceptions
            ]
            recoverable_exceptions.extend(backend_exceptions)

        except Exception as e:
            logger.exception(
                f'Failed to structure backend config for "{backend_id}" "{backend_type}"'
            )
            errors.append(
                ut.ParseError(
                    f'{type(e).__name__}: Failed to structure backend config for "{backend_id}" "{backend_type}": {e}'
                )
            )

    # Purge corrupted backends.
    for backend_id in corrupted_backends:
        del backend_data[backend_id]

    return backend_data, recoverable_exceptions, errors


def config_converter_factory() -> Converter:
    """
    Create a cattrs converter with the necessary overrides for the Config class.

    This is only used when unstructuring, as cattrs isn't fault tolerant enough when
    structuring and doesn't provide errors either.
    """
    converter = Converter()
    converter.register_unstructure_hook(bi.BackendConfig, attrs.asdict)
    return converter
