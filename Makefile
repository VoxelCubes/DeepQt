# define variables
PYTHON = venv/bin/python
CurrentDir := $(shell pwd)
BUILD_DIR = dist
BUILD_CACHE = deepqt.egg-info build
QRC_DIR_ICONS := icons
QRC_DIR_THEMES := themes
UI_DIR := ui_files
RC_OUTPUT_DIR := deepqt/rc_generated_files
UI_OUTPUT_DIR := deepqt/ui_generated_files
RCC_COMPILER := venv/bin/pyside6-rcc
UIC_COMPILER := venv/bin/pyside6-uic
BLACK_LINE_LENGTH := 120
BLACK_TARGET_DIR := deepqt/
BLACK_EXCLUDE_PATTERN := "^$(RC_OUTPUT_DIR)/.*|^$(UI_OUTPUT_DIR)/.*"

# default target
fresh-install: clean build install

refresh-assets: build-icon-cache compile-qrc compile-ui

# build target
build:
	$(PYTHON) -m build --outdir $(BUILD_DIR)

# install target
install:
	$(PYTHON) -m pip install $(BUILD_DIR)/*.whl

# clean target
clean:
	rm -rf $(BUILD_DIR)
	rm -rf $(BUILD_CACHE)
	rm -rf AUR/deepqt/pkg
	rm -rf AUR/deepqt/src
	rm -rf AUR/deepqt/*.tar.gz
	rm -rf AUR/deepqt/*.tar.zst

release:
	twine upload $(BUILD_DIR)/*

# compile .qrc files
compile-qrc:
	for file in $(QRC_DIR_ICONS)/*.qrc; do \
		basename=`basename $$file .qrc`; \
		$(RCC_COMPILER) $$file -o $(RC_OUTPUT_DIR)/rc_$$basename.py; \
	done
	for file in $(QRC_DIR_THEMES)/*.qrc; do \
		basename=`basename $$file .qrc`; \
		$(RCC_COMPILER) $$file -o $(RC_OUTPUT_DIR)/rc_$$basename.py; \
	done

# compile .ui files
compile-ui:
	for file in $(UI_DIR)/*.ui; do \
		basename=`basename $$file .ui`; \
		$(UIC_COMPILER) $$file -o $(UI_OUTPUT_DIR)/ui_$$basename.py; \
	done

# run build_icon_cache.py
build-icon-cache:
	cd $(QRC_DIR_ICONS) && ${CurrentDir}/$(PYTHON) build_icon_cache.py
	cd $(QRC_DIR_ICONS)/custom_icons && ${CurrentDir}/$(PYTHON) copy_from_dark_to_light.py

# format the code
black-format:
	find $(BLACK_TARGET_DIR) -type f -name '*.py' | grep -Ev $(BLACK_EXCLUDE_PATTERN) | xargs black --line-length $(BLACK_LINE_LENGTH)

.PHONY: clean build install fresh-install release black-format compile-qrc compile-ui build-icon-cache refresh-assets