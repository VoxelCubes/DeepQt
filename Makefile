# define variables
PYTHON = venv/bin/python
CurrentDir := $(shell pwd)
BUILD_DIR = dist
BUILD_CACHE = deepqt.egg-info build
DIR_ICONS := icons
UI_DIR := ui_files
UI_OUTPUT_DIR := deepqt/ui_generated_files
UIC_COMPILER := venv/bin/pyside6-uic
BLACK_LINE_LENGTH := 100
BLACK_TARGET_DIR := deepqt/
BLACK_EXCLUDE_PATTERN := "^$(UI_OUTPUT_DIR)/.*"

# default target
fresh-install: clean build install

refresh-assets: build-icon-cache compile-ui

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

release: confirm
	$(PYTHON) -m twine upload $(BUILD_DIR)/*

# compile .ui files
compile-ui:
	for file in $(UI_DIR)/*.ui; do \
		basename=`basename $$file .ui`; \
		$(UIC_COMPILER) $$file -o $(UI_OUTPUT_DIR)/ui_$$basename.py; \
	done

build-icon-cache:
	$(PYTHON) $(DIR_ICONS)/build_icon_cache.py
	$(PYTHON) $(DIR_ICONS)/copy_from_dark_to_light.py
# format the code
black-format:
	find $(BLACK_TARGET_DIR) -type f -name '*.py' | grep -Ev $(BLACK_EXCLUDE_PATTERN) | xargs black --line-length $(BLACK_LINE_LENGTH)

confirm:
	@read -p "Are you sure you want to proceed? (yes/no): " CONFIRM; \
	if [ "$$CONFIRM" = "yes" ]; then \
		echo "Proceeding..."; \
	else \
		echo "Aborted by user."; \
		exit 1; \
	fi

.PHONY: confirm clean build install fresh-install release black-format compile-ui build-icon-cache refresh-assets