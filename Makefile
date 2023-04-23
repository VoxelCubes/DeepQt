# define variables
PYTHON = python
BUILD_DIR = dist/
BUILD_CACHE = deepqt.egg-info/

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


.PHONY: clean build install fresh-install release