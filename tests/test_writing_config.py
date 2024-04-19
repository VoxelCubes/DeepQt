import json

from loguru import logger

from tests.helpers import mock_file_path
from tests import mock_files
import tests.mock_files.config as config_files

import deepqt.config as cfg
import deepqt.constants as ct

# Suppress the loguru logger.
logger.remove()


def test_un_structuring():
    # We shouldn't find any attributes that have the "no_save" metadata flag set.
    # All other attributes should be present.

    config: cfg.Config = cfg.Config()

    dump: dict = config.dump()

    # First check the top level attributes.
    assert dump["gui_theme"] == config.gui_theme
    assert dump["lang_from"] == config.lang_from
    assert dump["lang_to"] == config.lang_to
    assert dump["last_backend"] == config.last_backend

    # Check all backend configs.
    for backend, bconf in config.backend_configs.items():
        backend_dump = dump["backend_configs"][backend]
        metadata = bconf.attribute_metadata()

        for attr, meta in metadata.items():
            if meta.no_save:
                assert attr not in backend_dump
            else:
                assert backend_dump[attr] == getattr(bconf, attr)
