#!/usr/bin/env python3
"""
Purpose:
This script is designed to create sparse copies of theme directories based on the structure specified in a YAML file.
It aims to extract only the essential files as defined in the YAML file and replicate the directory structure in the
current working directory. Additionally, the script generates a Qt resource file (theme_icons.qrc), which lists all
the copied files, making it convenient for use in Qt applications.

This only works on Linux systems that have Qt theme icons installed.

The YAML file must include two sections:
1. Theme directories: A list of the absolute paths to the theme directories.
2. Files: A dictionary that represents the structure of the files to be copied.
   It should contain the category, subcategory, and a list of filenames.
   

Example:
```
Theme directories:
    - /usr/share/icons/breeze
    - /usr/share/icons/breeze-dark
Files:
    actions:
        16:
            - document-new.svg
            - document-open.svg
            - document-save.svg
    
    apps:
        16:
            - kcalc.svg
            - kcharselect.svg
    
    mimetypes:
        16:
            - text-plain.svg
            - text-x-generic.svg
```


The script performs the following tasks:
1. Parse the YAML file to obtain the theme directory paths and file structure.
2. Create sparse copies of the theme directories, copying only the specified files.
3. Generate the theme_icons.qrc file, listing all the copied files with their relative paths.

Usage:
- Make sure the YAML file with the desired structure is in the current working directory and named "theme_list.yaml".
- Run the script, being aware of your current working directory, as that is where the file will go.

Requirements:
- Python 3.6 or higher
- PyYAML library
"""


import shutil
from pathlib import Path
import xml.etree.ElementTree as ET
import yaml

SUPPORTED_EXTENSIONS = [".svg", ".png", ".xpm"]


def parse_yaml_file(filename: Path) -> dict:
    """
    Parse the specified YAML file.

    :param filename: Path to the YAML file.
    :return: Parsed YAML data as a dictionary.
    """
    with filename.open("r") as file:
        return yaml.safe_load(file)


def find_xdg_icon(file, src_path, extensions) -> str | None:
    og_file = file
    # Loop through all allowed file extensions
    for ext in extensions:
        # Perform an XDG conformant search for the file
        while not (src_path / f"{file}{ext}").exists() and file:
            file = "-".join(file.split("-")[:-1])

        if file:
            return f"{file}{ext}"

        # Reset file name for the next iteration
        file = og_file

    # If the loop finishes without finding a file, return None
    return None


def is_icon_light(icon_path: Path) -> bool:
    """
    Check if the icon is actually dark by reading the file contents.
    Dark means that the text is light, as in this icon is for a dark background.

    :param icon_path: Path to the icon file.
    :return: True if the icon is dark, False otherwise.
    """
    with icon_path.open("rb") as f:
        content = f.read()

    # Check if the content contains the dark color.
    return b"#232629" in content


def make_icon_dark(icon_path: Path, output_path: Path) -> None:
    """
    Find the style tag and change the text color to dark.

    Example:
    <style type="text/css" id="current-color-scheme">.ColorScheme-Text{color:#fcfcfc;}</style>
    to:
    <style type="text/css" id="current-color-scheme">.ColorScheme-Text{color:#232629;}</style>
    """
    # Just do a string replacement.
    with icon_path.open("r") as f:
        content = f.read()

    content_old = content
    content = content.replace("#232629", "#fcfcfc")

    if content_old != content:
        print(f"Changed {icon_path.name} to dark.")
    else:
        print(f"Failed to change {icon_path.name} to dark.")

    with output_path.open("w") as f:
        f.write(content)


def copy_files(theme_dir: Path, yaml_data: dict) -> None:
    """
    Copy the specified files from the source theme directory to the destination directory.

    :param theme_dir: Path to the source theme directory.
    :param yaml_data: Dictionary containing the files to copy.
    """
    theme_is_dark = "dark" in theme_dir.name.lower()

    for category, subcategories in yaml_data["Files"].items():
        for subcategory, files in subcategories.items():
            src_path = theme_dir / str(category) / str(subcategory)
            dest_path = Path.cwd() / theme_dir.name / str(category) / str(subcategory)

            if not dest_path.exists():
                dest_path.mkdir(parents=True)

            for file in files:
                found_file = find_xdg_icon(file, src_path, SUPPORTED_EXTENSIONS)

                if found_file:
                    # Check if the file is mis-colored.
                    if theme_is_dark and found_file.endswith(".svg"):
                        found_file_path = src_path / found_file
                        dest_file_path = dest_path / found_file

                        if is_icon_light(found_file_path):
                            make_icon_dark(found_file_path, dest_file_path)
                        else:
                            print(f"Not recoloring {found_file} as it is already dark.")
                            shutil.copy2(src_path / found_file, dest_path)

                    else:
                        shutil.copy2(src_path / found_file, dest_path)
                else:
                    print(f"Could not find {file} in {src_path}")


def create_sparse_copy(theme_dir: Path, yaml_data: dict) -> None:
    """
    Create a sparse copy of the theme directory in the current working directory.

    :param theme_dir: Path to the source theme directory.
    :param yaml_data: Dictionary containing the files to copy.
    """
    dest_dir = Path.cwd() / theme_dir.name

    if dest_dir.exists():
        shutil.rmtree(dest_dir)

    dest_dir.mkdir()

    shutil.copy2(theme_dir / "index.theme", dest_dir)

    copy_files(theme_dir, yaml_data)


def generate_qrc_file(yaml_data: dict) -> None:
    """
    Generate the theme_icons.qrc file based on the copied files.

    :param yaml_data: Dictionary containing the files to include in the qrc file.
    """
    qrc_file = Path.cwd() / "theme_icons.qrc"

    with qrc_file.open("w") as f:
        f.write("<RCC>\n")
        f.write('  <qresource prefix="icon-themes">\n')

        for theme_dir_str in yaml_data["Theme directories"]:
            theme_dir = Path(theme_dir_str)
            dest_dir = Path.cwd() / theme_dir.name

            f.write(f"    <file>{dest_dir.relative_to(Path.cwd())}/index.theme</file>\n")

            for category, subcategories in yaml_data["Files"].items():
                for subcategory, files in subcategories.items():
                    src_path = theme_dir / str(category) / str(subcategory)

                    for file in files:
                        found_file = find_xdg_icon(file, src_path, SUPPORTED_EXTENSIONS)

                        if found_file:
                            f.write(
                                f"    <file>{dest_dir.relative_to(Path.cwd())}/{str(category)}/{str(subcategory)}/{found_file}</file>\n"
                            )
                        else:
                            print(f"Could not find {file} in {src_path}")

        f.write("  </qresource>\n")
        f.write("</RCC>\n")


def main() -> None:
    """
    Main function to create sparse copies of theme directories based on the specified YAML file and generate theme_icons.qrc.
    """
    yaml_filename = Path("theme_list.yaml")
    yaml_data = parse_yaml_file(yaml_filename)

    for theme_dir_str in yaml_data["Theme directories"]:
        theme_dir = Path(theme_dir_str)
        create_sparse_copy(theme_dir, yaml_data)

    generate_qrc_file(yaml_data)


if __name__ == "__main__":
    main()
