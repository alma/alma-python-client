VIRTUALENV = virtualenv --python=python3

VENV := $(shell echo $${VIRTUAL_ENV-.venv})
PYTHON = $(VENV)/bin/python

INSTALL_STAMP = $(VENV)/.install.stamp
DEV_STAMP = $(VENV)/.dev_env_installed.stamp
TEMPDIR := $(shell mktemp -du)

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  format                      reformat code: black and isort"
	@echo "  install                     install dependencies and prepare environment"
	@echo "  install-dev                 install dependencies and everything needed to run tests"
	@echo "  black                       run the black tool, which will automatically reformat the code"
	@echo "  isort                       run the isort tool, which will automatically sort all of the imports"
	@echo "  clean                       remove *.pyc files and __pycache__ directory"
	@echo "  distclean                   remove *.egg-info files and *.egg, build and dist directories"
	@echo "  maintainer-clean            remove the .tox and the .venv directories"
	@echo "Check the Makefile to know exactly what each target is doing."

virtualenv: $(PYTHON)
$(PYTHON):
	$(VIRTUALENV) $(VENV)

install: $(INSTALL_STAMP)
$(INSTALL_STAMP): $(PYTHON) setup.py requirements.txt
	$(VENV)/bin/pip install -U pip
	$(VENV)/bin/pip install -Ue . -c requirements.txt
	touch $(INSTALL_STAMP)

install-dev: $(INSTALL_STAMP) $(DEV_STAMP)
$(DEV_STAMP): $(PYTHON) dev-requirements.txt
	$(VENV)/bin/pip install -Ur dev-requirements.txt
	touch $(DEV_STAMP)

format: black isort

black: install-dev
	$(VENV)/bin/black setup.py alma

isort: install-dev
	$(VENV)/bin/isort --recursive setup.py alma tests

flake8: install-dev
	$(VENV)/bin/flake8 setup.py alma tests

mypy: install-dev
	$(VENV)/bin/mypy --ignore-missing-imports --scripts-are-modules alma

build-requirements:
	$(VIRTUALENV) $(TEMPDIR)
	$(TEMPDIR)/bin/pip install -U pip
	$(TEMPDIR)/bin/pip install -Ue .
	$(TEMPDIR)/bin/pip freeze | grep -v -- '-e' > requirements.txt

clean:
	find . -name '__pycache__' -type d | xargs rm -fr

distclean: clean
	rm -fr *.egg *.egg-info/ dist/ build/

maintainer-clean: distclean
	rm -fr .venv/ .tox/
