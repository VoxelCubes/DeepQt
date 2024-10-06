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
                    value = converter.unstructure(value)
                result[field.name] = value
            return result

        converter.register_unstructure_hook(bi.BackendConfig, censor_keys_hook)

        # Using yaml safe dump to avoid having any object constructors in the output.
        # Convert all Backend string enums to their base string, so safe_dump can handle them.

        # TODO This piece of shit won't unstructure the damn Backend enums.
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


def load_config(
    conf_path: Path, config_factory: Callable[[], Any] = Config
) -> tuple[Config, bool, list[ut.ParseException]]:
    """
    Load the configuration from the given path.
    If no errors occur, return the config, True, and an empty list.
    If a critical error occurs, return the config, False, and the error.
    If non-critical errors occur, return the config, True, and the errors.

    :param conf_path: Path to the configuration file.
    :param config_factory: [Optional] Factory function to create a new config object.
    :return: The configuration, whether it was loaded successfully (fully or in part), and any errors.
    """

    config = config_factory()

    success = True
    errors: list[ut.ParseException]

    try:
        with open(conf_path, "r") as f:
            # Load the default config, then update it with the values from the config file.
            # This way, missing values will be filled in with the default values.
            json_data = json.load(f)

            errors = ut.load_dict_to_attrs_safely(config, json_data, skip_attrs=["backend_configs"])

            if "backend_configs" in json_data:
                # Attempt to structure the json data into the correct backend config class,
                # based on the backend type.
                backend_configs, backend_errors, critical_failure = structure_backend_configs(
                    json_data["backend_configs"]
                )
                config.backend_configs.update(backend_configs)
                errors.extend(backend_errors)
                if critical_failure:
                    success = False
    except OSError as e:
        logger.exception(f"Failed to read config file {conf_path}")
        errors = [
            ut.ParseException(f"{type(e).__name__}: Failed to read config file {conf_path}: {e}")
        ]
        success = False
    except json.decoder.JSONDecodeError as e:
        logger.exception(f"Configuration file could not be parsed {conf_path}")
        errors = [
            ut.ParseException(
                f"{type(e).__name__}: Configuration file could not be parsed {conf_path}: {e}"
            )
        ]
        success = False

    # If fubar, reset the config just to be sure.
    if not success:
        config = config_factory()

    return config, success, errors


def structure_backend_configs(
    json_data: dict[int, dict]
) -> tuple[dict[bi.BackendID, bi.BackendConfig], list[ut.ParseException], bool]:
    """
    Attempt to structure the json data into the correct backend config class,
    based on the backend type in the id.

    If the error list is empty, no exceptions occurred.

    :param json_data: The json data to structure.
    :return: The structured backend configs and any errors that occurred and if a critical failure occurred.
    """
    errors: list[ut.ParseException] = []
    json_keys = list(json_data.keys())
    backend_data: dict[bi.BackendID, bi.BackendConfig | dict] = {}
    critical_failure = False

    # Cast the key ints to the BackendID type.
    # It honestly doesn't matter what type they are, as long as they're hashable,
    # which they are, coming from json.
    for backend_id in json_keys:
        backend_data[bi.BackendID(backend_id)] = json_data[backend_id]

    for backend_id in backend_data:
        try:
            # Look into the backend_type field to determine the backend type.
            backend_type = ct.Backend(json_data[backend_id]["backend_type"])
        except KeyError:
            logger.error(f"Backend {backend_id} has no backend_type field")
            errors.append(
                ut.ParseException(
                    f"Backend {backend_id} has no backend_type field. The backend could not be loaded!"
                )
            )
            critical_failure = True
            continue
        except ValueError:
            logger.error(f"Unknown backend: {backend_id}")
            errors.append(ut.ParseException(f"Unknown backend: {backend_id}"))
            critical_failure = True
            continue

        # Because the string and the strenum hashes are identical and Python treats them as equal,
        # we can simply ask the json_data using the strenum as a key as well.
        # Alternatively, to be fully correct, use backend.value but the static type checker
        # didn't like it for some reason, likely a false positive.
        try:
            config_obj = b_lut.backend_to_config[backend_type]
            backend_data[backend_id], backend_errors = config_obj.from_dict(
                backend_data[backend_id]
            )
            errors.extend(backend_errors)

        except Exception as e:
            logger.exception(f"Failed to structure backend config for {backend_id} {backend_type}")
            errors.append(
                ut.ParseException(
                    f"{type(e).__name__}: Failed to structure backend config for {backend_id} {backend_type}: {e}"
                )
            )

    return backend_data, errors, critical_failure


def config_converter_factory() -> Converter:
    """
    Create a cattrs converter with the necessary overrides for the Config class.

    This is only used when unstructuring, as cattrs isn't fault tolerant enough when
    structuring and doesn't provide errors either.
    """
    converter = Converter()
    converter.register_unstructure_hook(bi.BackendConfig, attrs.asdict)
    return converter
