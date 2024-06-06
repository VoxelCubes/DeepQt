import deepqt.constants as ct
import deepqt.backends.mock_backend as mb
import deepqt.backends.deepl_backend as db

# This is a mapping of backend names to their respective classes.
# File separated out to prevent circular imports.

backend_to_config = {
    ct.Backend.MOCK: mb.MockConfig,
    ct.Backend.DEEPL: db.DeepLConfig,
}

backend_to_class = {
    ct.Backend.MOCK: mb.MockBackend,
    ct.Backend.DEEPL: db.DeepLBackend,
}
