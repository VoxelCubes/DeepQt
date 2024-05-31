import deepqt.constants as ct
import deepqt.backends.mock_backend as mb
import deepqt.backends.deepl_backend as db

backend_to_config = {
    ct.Backend.MOCK: mb.MockConfig,
    ct.Backend.DEEPL: db.DeepLConfig,
}
