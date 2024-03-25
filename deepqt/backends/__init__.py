import deepqt.backends.backend_interface as bi
import deepqt.backends.deepl_backend as db
import deepqt.backends.mock_backend as mb
import deepqt.constants as ct


def get_backend(backend: ct.Backend) -> bi.ReliableBackend | bi.UnreliableBackend:
    if backend == ct.Backend.MOCK:
        return mb.MockBackend()
    elif backend == ct.Backend.DEEPL:
        return db.DeepLBackend()
    else:
        raise ValueError(f"Backend {backend} not supported")
