.PHONY: clean clean-build clean-pyc clean-test coverage dist docs help install check format {%- if cookiecutter.use_release_helpers == 'y' %}bump-version release{%- endif %}
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

PYTHON ?= python
CYTHON ?= cython
PYTEST ?= uv run pytest
CTAGS ?= ctags
PIP ?= uv pip
MAKE ?= make
PRECOMMIT ?= uv run pre-commit
RUFF ?= uv run ruff
MYPY ?= uv run mypy
ISORT ?= uv run isort
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc {%- if cookiecutter.use_pytest == 'y' %}clean-test{%- endif %} ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

{%- if cookiecutter.use_ruff_format == 'y' %}
ruff: ## run ruff as a formatter
	$(RUFF) check --fix --silent --exit-zero {{ cookiecutter.project_slug }}
	$(RUFF) check --fix --exit-zero --no-cache {{ cookiecutter.project_slug }}
isort:
	$(ISORT) {{ cookiecutter.project_slug }} tests
{%- endif %}
{%- if cookiecutter.use_mypy_typing == 'y' %}
typing: ## run ruff as a formatter
	$(MYPY) {{ cookiecutter.project_slug }} tests
{%- endif %}
test: ## run tests quickly with the default Python
{%- if cookiecutter.use_pytest == 'y' %}
	$(PYTEST) tests
{%- else %}
	python setup.py tests
{%- endif %}
{%- if cookiecutter.use_pytest == 'y' %}
cov-report:
	coverage html -d coverage_html
{%- endif %}

coverage: ## check code coverage quickly with the default Python
{%- if cookiecutter.use_pytest == 'y' %}
	coverage run --source {{ cookiecutter.project_slug }} -m pytest
{%- else %}
	coverage run --source {{ cookiecutter.project_slug }} setup.py test
{%- endif %}
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html
{%- if cookiecutter.use_docs == 'y' %}
docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/{{ cookiecutter.project_slug }}.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ {{ cookiecutter.project_slug }}
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html
{%- endif %}
{%- if cookiecutter.use_release_helpers == 'y' %}
bump-version: ## bump the version -- add current version number and kind of upgrade (minor, major, patch) as arguments
	bump-my-version bump --current-version

release: dist ## package and upload a release
	twine upload --repository testpypi dist/*
	@echo
	@echo "Test with the following:"
	@echo "* Create a new virtual environment to install the uploaded distribution into"
	@echo "* Run the following:"
	@echo
	@echo "        pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ {{cookiecutter.project_slug}}"
	@echo
	@echo "* Run this to make sure it can import correctly, plus whatever else you'd like to test:"
	@echo
	@echo "        python -c 'import {{cookiecutter.project_slug}}'"
	@echo
	@echo "Once you have decided it works, publish to actual pypi with"
	@echo
	@echo "    python -m twine upload dist/*"

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist
{%- endif %}
install: clean ## install the package to the active Python's site-packages
	$(PIP) install -e ".[dev]"

pre-commit:
	$(PRECOMMIT) run --all-files

format:
	make ruff
	make isort
	{%- if cookiecutter.use_mypy_typing == 'y' %}
	make typing
	{%- endif %}