# DeepQt

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI version](https://img.shields.io/pypi/v/deepqt)](https://pypi.org/project/deepqt/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Harness the power of the DeepL API with this friendly user interface.

![](/media/example_screenshot.png)

## Features

- Batch processing.

- Higher-level glossaries. [How do they work?](https://github.com/VoxelCubes/DeepQt/blob/master/docs/glossary_help.md)
  Apply replacements even without translating any of the text.

- Support for text files (epub coming eventually)

## Requires

- A DeepL API license, either free or pro. [How do I get this?](https://github.com/VoxelCubes/DeepQt/blob/master/docs/api_help.md)

- A Python installation, version **3.10** or higher. On Linux you will probably already have this installed. On Windows, you will likely need to set it up. [Download Python | Python.org](https://www.python.org/downloads/) or use your package manager (apt, pacman, dnf, chocolatey, winget etc.)

## Installation

Download the latest release from [PyPi](https://pypi.org/project/deepqt/).

```
pip install deepqt
```
Run it with `deepqt` from the terminal.

Or download a prepackaged format from the [releases](https://github.com/VoxelCubes/DeepQt/releases/latest) page:

- .whl (Manual pip installation)
- .elf (Linux)
- .exe (Windows)

## Roadmap


- [ ] Support .epub files for translation.

- [ ] Build AppImage or Flatpak.
