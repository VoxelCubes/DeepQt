import json

from loguru import logger

from tests.helpers import mock_file_path
from tests import mock_files
import tests.mock_files.config as config_files

import deepqt.config as cfg
import deepqt.constants as ct

# Suppress the loguru logger.
logger.remove()


def test_good():
    # Should load values from file.
    path = mock_file_path("good.json", module=config_files)
    config, success, errors = cfg.load_config(path)

    assert success
    assert not errors
    assert isinstance(config, cfg.Config)
    assert config.lang_from == "Valid language code"
    assert config.use_glossary is True
    assert config.backend_configs[ct.Backend.MOCK].avg_time_per_mille == -9000


def test_coercible_types():
    # Should load values from file.
    path = mock_file_path("coercible_types.json", module=config_files)
    config, success, errors = cfg.load_config(path)

    assert success
    assert not errors
    assert isinstance(config, cfg.Config)
    assert config.lang_from == "Valid language code"
    assert config.use_glossary is True
    assert config.backend_configs[ct.Backend.MOCK].avg_time_per_mille == -2
    assert config.backend_configs[ct.Backend.MOCK].chunk_size == 1000
    assert isinstance(config.backend_configs[ct.Backend.MOCK].chunk_size, int)
    assert config.backend_configs[ct.Backend.DEEPL].tl_preserve_formatting is True


def test_empty():
    # Should return default config.
    path = mock_file_path("empty.json", module=config_files)
    config, success, errors = cfg.load_config(path)

    assert success
    assert not errors
    assert isinstance(config, cfg.Config)
    default_config = cfg.Config()
    assert config.lang_from == default_config.lang_from
    assert config.use_glossary == default_config.use_glossary
    assert (
        config.backend_configs[ct.Backend.MOCK].avg_time_per_mille
        == default_config.backend_configs[ct.Backend.MOCK].avg_time_per_mille
    )


def test_blank():
    # Should return a JSONDecodeError and no success.
    path = mock_file_path("blank_file")
    _, success, errors = cfg.load_config(path)

    assert not success
    assert len(errors) == 1
    assert str(errors[0]).startswith("JSONDecodeError")


def test_invalid():
    # Should return a JSONDecodeError and no success.
    path = mock_file_path("invalid.json", module=config_files)
    _, success, errors = cfg.load_config(path)

    assert not success
    assert len(errors) == 1
    assert str(errors[0]).startswith("JSONDecodeError")


def test_missing_and_extra_keys():
    # Should succeed but retain default values for certain attributes.
    path = mock_file_path("missing_and_extra_keys.json", module=config_files)
    config, success, errors = cfg.load_config(path)

    default_config = cfg.Config()

    assert success
    assert not errors
    assert isinstance(config, cfg.Config)
    assert config.lang_from == "Valid language code"
    assert "nonsense" not in config.__annotations__
    assert config.use_glossary == default_config.use_glossary
    assert (
        config.backend_configs[ct.Backend.MOCK].wait_time
        == default_config.backend_configs[ct.Backend.MOCK].wait_time
    )
    assert "more nonsense" not in config.backend_configs[ct.Backend.MOCK].__annotations__
    assert (
        config.backend_configs[ct.Backend.MOCK].name
        == default_config.backend_configs[ct.Backend.MOCK].name
    )


def test_missing_backend():
    # Should succeed but retain default values for certain attributes.
    path = mock_file_path("missing_backend.json", module=config_files)
    config, success, errors = cfg.load_config(path)

    default_config = cfg.Config()

    assert success
    assert not errors
    assert isinstance(config, cfg.Config)
    assert config.lang_from == "Valid language code"
    assert config.use_glossary == default_config.use_glossary
    assert (
        config.backend_configs[ct.Backend.MOCK].wait_time
        == default_config.backend_configs[ct.Backend.MOCK].wait_time
    )
    assert (
        config.backend_configs[ct.Backend.DEEPL].tl_preserve_formatting
        == default_config.backend_configs[ct.Backend.DEEPL].tl_preserve_formatting
    )


def test_type_mismatch():
    # Should succeed, but result in several type errors, leaving default values in place.
    path = mock_file_path("type_mismatch.json", module=config_files)
    config, success, errors = cfg.load_config(path)

    default_config = cfg.Config()

    assert success
    assert len(errors) == 2
    assert str(errors[0]).startswith("ValueError")
    assert str(errors[1]).startswith("TypeError")
    assert isinstance(config, cfg.Config)
    assert config.lang_from == "Valid language code"
    assert config.use_glossary == default_config.use_glossary
    assert (
        config.backend_configs[ct.Backend.MOCK].wait_time
        == default_config.backend_configs[ct.Backend.MOCK].wait_time
    )


def test_unknown_backend():
    # Should succeed, but result in an error for the unknown backend.
    path = mock_file_path("unknown_backend.json", module=config_files)
    config, success, errors = cfg.load_config(path)

    assert success
    assert len(errors) == 1
    assert str(errors[0]).startswith("Unknown backend")
    assert isinstance(config, cfg.Config)
    assert config.backend_configs[ct.Backend.DEEPL].wait_time == 42
