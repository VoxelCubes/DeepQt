from loguru import logger

import deepqt.backends.backend_interface as bi
import deepqt.backends.mock_backend as mock_b
import deepqt.config as cfg
import tests.mock_files.config as config_files
from tests.helpers import mock_file_path


# Suppress the loguru logger.
logger.remove()


def test_good():
    # Should load values from file.
    path = mock_file_path("good.json", module=config_files)
    config, recoverable_exceptions, errors, critical_errors = cfg.load_config(path)
    success = not any((recoverable_exceptions, errors, critical_errors))

    assert success
    assert isinstance(config, cfg.Config)
    assert config.lang_from == "Valid language code"
    assert config.use_glossary is True
    assert config.backend_configs[bi.BackendID("0")].avg_time_per_mille == -9000


def test_coercible_types():
    # Should load values from file.
    path = mock_file_path("coercible_types.json", module=config_files)
    config, recoverable_exceptions, errors, critical_errors = cfg.load_config(path)
    success = not any((recoverable_exceptions, errors, critical_errors))

    assert success
    assert isinstance(config, cfg.Config)
    assert config.lang_from == "Valid language code"
    assert config.use_glossary is True
    assert config.backend_configs[bi.BackendID("0")].avg_time_per_mille == -2
    assert config.backend_configs[bi.BackendID("0")].chunk_size == 1000
    assert isinstance(config.backend_configs[bi.BackendID("0")].chunk_size, int)
    assert config.backend_configs[bi.BackendID("1")].tl_preserve_formatting is True


def test_empty():
    # Should return default config.
    path = mock_file_path("empty.json", module=config_files)
    config, recoverable_exceptions, errors, critical_errors = cfg.load_config(path)
    success = not any((recoverable_exceptions, errors, critical_errors))

    assert success
    assert isinstance(config, cfg.Config)
    default_config = cfg.Config()
    assert config.lang_from == default_config.lang_from
    assert config.use_glossary == default_config.use_glossary
    assert config.backend_configs == default_config.backend_configs


def test_blank():
    # Should return a JSONDecodeError and no success.
    path = mock_file_path("blank_file")
    _, recoverable_exceptions, errors, critical_errors = cfg.load_config(path)
    success = not any((recoverable_exceptions, errors, critical_errors))

    assert not success
    assert not recoverable_exceptions
    assert not errors
    assert len(critical_errors) == 1
    assert str(critical_errors[0]).startswith("JSONDecodeError")


def test_invalid():
    # Should return a JSONDecodeError and no success.
    path = mock_file_path("invalid.json", module=config_files)
    _, recoverable_exceptions, errors, critical_errors = cfg.load_config(path)
    success = not any((recoverable_exceptions, errors, critical_errors))

    assert not success
    assert not recoverable_exceptions
    assert not errors
    assert len(critical_errors) == 1
    assert str(critical_errors[0]).startswith("JSONDecodeError")


def test_missing_and_extra_keys():
    # Should succeed but retain default values for certain attributes.
    path = mock_file_path("missing_and_extra_keys.json", module=config_files)
    config, recoverable_exceptions, errors, critical_errors = cfg.load_config(path)
    success = not any((recoverable_exceptions, errors, critical_errors))

    default_config = cfg.Config()
    default_config_mock = mock_b.MockConfig()

    assert success
    assert isinstance(config, cfg.Config)
    assert config.lang_from == "Valid language code"
    assert "nonsense" not in config.__annotations__
    assert config.use_glossary == default_config.use_glossary
    assert len(config.backend_configs) == 2
    assert config.backend_configs[bi.BackendID("0")].wait_time == default_config_mock.wait_time
    assert "more nonsense" not in config.backend_configs[bi.BackendID("0")].__annotations__
    assert config.backend_configs[bi.BackendID("0")].name == default_config_mock.name
    assert config.backend_configs[bi.BackendID("0")].help != "This should never be here"


def test_missing_backend():
    # Should succeed but retain default values for certain attributes.
    path = mock_file_path("missing_backend.json", module=config_files)
    config, recoverable_exceptions, errors, critical_errors = cfg.load_config(path)
    success = not any((recoverable_exceptions, errors, critical_errors))

    default_config = cfg.Config()

    assert success
    assert isinstance(config, cfg.Config)
    assert config.lang_from == "Valid language code"
    assert config.use_glossary == default_config.use_glossary
    assert len(config.backend_configs) == 0


def test_type_mismatch():
    # Should succeed, but result in several type errors, leaving default values in place.
    path = mock_file_path("type_mismatch.json", module=config_files)
    config, recoverable_exceptions, errors, critical_errors = cfg.load_config(path)
    success = not any((recoverable_exceptions, errors, critical_errors))

    default_config = cfg.Config()
    default_config_mock = mock_b.MockConfig()

    assert not success
    assert len(recoverable_exceptions) == 2
    assert not errors
    assert not critical_errors
    assert str(recoverable_exceptions[0]).startswith('Backend "0": ValueError')
    assert str(recoverable_exceptions[1]).startswith('Backend "1": TypeError')
    assert isinstance(config, cfg.Config)
    assert config.lang_from == "Valid language code"
    assert config.use_glossary == default_config.use_glossary
    assert config.backend_configs[bi.BackendID("0")].wait_time == default_config_mock.wait_time


def test_unknown_backend():
    # Should succeed, but result in an error for the unknown backend.
    path = mock_file_path("unknown_backend.json", module=config_files)
    config, recoverable_exceptions, errors, critical_errors = cfg.load_config(path)
    success = not any((recoverable_exceptions, errors, critical_errors))

    assert not success
    assert not recoverable_exceptions
    assert not critical_errors
    assert len(errors) == 2
    assert str(errors[0]).startswith("Unknown backend")
    assert (
        str(errors[1])
        == 'Backend "Missing backend type" has no backend_type field. The backend could not be loaded!'
    )
    assert isinstance(config, cfg.Config)
    assert len(config.backend_configs) == 1
    assert config.backend_configs[bi.BackendID("1")].wait_time == 42
