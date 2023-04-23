# define variables
PROJECT = deepqt
PYTHON = python
BUILD_DIR = dist/
BUILD_CACHE = deepqt.egg-info/
FLATPAK_PROJECT = com.voxel.deepqt
FLATPAK_SOURCE_DIR = .flatpak/flatpak_sources
FLATPAK_BASE_DIR = .flatpak
FLATPAK_BUILD_DIR = .flatpak/build-dir
FLATPAK_REPO_DIR = .flatpak/repo
FLATPAK_PYTHON_PACKAGE_DIR = $(FLATPAK_SOURCE_DIR)/python-packages


# default target
fresh-install: clean build install

# build target
build:
	$(PYTHON) -m build --outdir $(BUILD_DIR)

# install target
install:
	$(PYTHON) -m pip install $(BUILD_DIR)*.whl

# clean target
clean:
	rm -rf $(BUILD_DIR)
	rm -rf $(BUILD_CACHE)

release:
	twine upload $(BUILD_DIR)*

# flatpak targets
prepare-flatpak: clean-flatpak
	mkdir -p $(FLATPAK_BUILD_DIR) $(FLATPAK_REPO_DIR)
	mkdir -p $(FLATPAK_SOURCE_DIR)
	pip download -r requirements.txt --dest $(FLATPAK_PYTHON_PACKAGE_DIR)
    # Also build the current package to the dependencies folder.
	$(PYTHON) -m build --outdir $(FLATPAK_PYTHON_PACKAGE_DIR)
	# Include the desktop file and the icon in the flatpak.
	cp ./media/deepqt.png $(FLATPAK_SOURCE_DIR)/deepqt.png
	cp ./DeepQt-flatpak.desktop $(FLATPAK_SOURCE_DIR)/DeepQt.desktop

build-flatpak: prepare-flatpak
	flatpak-builder --repo=$(FLATPAK_REPO_DIR) --force-clean $(FLATPAK_BUILD_DIR) $(FLATPAK_PROJECT).yaml
	@echo 'Building flatpak bundle, this may take a few minutes...'
	flatpak build-bundle $(FLATPAK_REPO_DIR) $(PROJECT).flatpak $(FLATPAK_PROJECT)
	rm -rf $(FLATPAK_BUILD_DIR)

install-flatpak: build-flatpak
	flatpak install --user --bundle $(PROJECT).flatpak
	flatpak run $(FLATPAK_PROJECT)

clean-flatpak:
	rm -rf .flatpak

.PHONY: clean build install fresh-install release prepare-flatpak build-flatpak clean-flatpak
