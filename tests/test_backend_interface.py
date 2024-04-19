from typing import get_type_hints
import deepqt.backends.backend_interface as bi
import deepqt.backends.mock_backend as mb
import deepqt.backends.deepl_backend as db


def check_attribute_metadata(some_thing: bi.BackendConfig | bi.BackendStatus):
    """
    Test some config class that inherits from BackendConfig or BackendStatus.
    (Not a test on its own, but a helper function for other tests.)
    """
    meta = some_thing.attribute_metadata()

    # Get attributes of the class and the base class.
    attributes = get_type_hints(some_thing)
    parent = some_thing.__class__.__bases__[0]
    attributes.update(get_type_hints(parent))

    # Check if all attributes are covered in the metadata.
    # for attr in attributes:
    #     if attr not in meta:
    #         raise ValueError(f"Attribute {attr} not covered in metadata")
    attr_names = list(attributes.keys())
    meta_names = list(meta.keys())

    # Check for duplicates.
    for name in attr_names:
        if attr_names.count(name) > 1:
            raise ValueError(f"Duplicate attribute name: {name}")
    for name in meta_names:
        if meta_names.count(name) > 1:
            raise ValueError(f"Duplicate metadata name: {name}")

    # Check for missing attributes.
    attr_names = set(attr_names)
    meta_names = set(meta_names)
    in_attr_not_in_meta = attr_names - meta_names
    in_meta_not_in_attr = meta_names - attr_names
    if in_attr_not_in_meta:
        raise ValueError(f"Attributes not covered in metadata: {in_attr_not_in_meta}")
    if in_meta_not_in_attr:
        raise ValueError(f"Metadata not covered in attributes: {in_meta_not_in_attr}")

    # Check the meta type matches the attribute type.
    for name in attr_names & meta_names:
        if meta[name].type != attributes[name]:
            raise ValueError(
                f"Type mismatch for attribute {name}: meta {meta[name].type} != actual {attributes[name]}"
            )


def test_mock():
    """
    Test the MockConfig.
    """
    check_attribute_metadata(mb.MockConfig())


def test_deepl():
    """
    Test the DeepLConfig.
    """
    check_attribute_metadata(db.DeepLConfig())
