import yaml
from pathlib import Path, PosixPath

import PySide6.QtCore as Qc

import deepqt.utils as ut
import deepqt.rc_generated_files.rc_themes
import deepqt.rc_generated_files.rc_theme_icons


def test_get_available_themes():
    """
    Test the get_available_themes function.
    """
    themes = ut.get_available_themes()

    assert themes
    assert themes == [("breeze", "Breeze Light"), ("breeze-dark", "Breeze Dark")]


def test_theme_icon_presence():
    """
    Test that all icons are present in the resources.
    """
    # Read the icon list from the yaml file located at DeepQt/icons/theme_list.yaml
    yaml_path = Path(__file__).parent.parent / "icons" / "theme_list.yaml"
    qrc_theme_icons = Qc.QDir(":/icon-themes/")

    with yaml_path.open() as file:
        data = yaml.safe_load(file)

    theme_directories = data["Theme directories"]
    theme_icons = data["Files"]

    # Perform a depth-first search for each icon in a theme, which means
    # checking for leaf nodes, which are the icon file names.
    # When coming across a directory, the name of that directory is added to the path,
    # then scanned recursively.
    for theme_path in theme_directories:
        # Only use the last directory name of the theme path.
        theme_directory = PosixPath(theme_path).name
        for category, sizes in theme_icons.items():
            for size, icons in sizes.items():
                for icon in icons:
                    expected_path = PosixPath(theme_directory) / category / str(size) / icon

                    for suffix in ["svg", "png"]:
                        if qrc_theme_icons.exists(expected_path.with_suffix(f".{suffix}").as_posix()):
                            break
                    else:
                        assert False, f"Icon {expected_path} not found in the theme_icons.qrc file."
