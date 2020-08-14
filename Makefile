.DEFAULT_GOAL := help
export VENV := $(abspath venv)
export PATH := ${VENV}/bin:${PATH}

.PHONY: help
help:				## Prints the help message.
	@echo "Usage:"; \
	awk -F ':|##' '/^[^\t].+?:.*?##/ {\
		printf "\033[36m  make %-30s\033[0m %s\n", $$1, $$NF \
	}' $(MAKEFILE_LIST)

.PHONY: clean-venv
clean-venv:			## Cleans the venv directory.
	rm -rf ./venv;

.PHONY: create-venv
create-venv: clean-venv		## Creates the venv directory.
	python3 -m venv venv;

.PHONY: dev
dev:				## Creates the dev environment.
	pip install -Ur requirements_dev.txt; \
	pip install -Ur requirements_test.txt; \
	pre-commit install;

.PHONY: test
test:				## Tests the project.
	pytest tests/ --cov=pygtt/ --cov-report term-missing;

.PHONY: install
install: 			## Installs the package to the active Python's site-packages.
	pip install -Ur requirements.txt; \
	pip install -e .;

.PHONY: build
build:				## Builds the package
	rm -rf dist/
	python3 setup.py sdist

.PHONY: release		## Releases the package
release:
	twine upload dist/*
