PROJ_DIR="`pwd`"
SYSTEM_PYTHON=python3
VENV_PYTHON="${PROJ_DIR}/venv/bin/python3"
SOURCE_DIR="${PROJ_DIR}"
APP_ENTRYPOINT="${SOURCE_DIR}/air_quality"


virtualenv:
	@echo "Installing virtualenv if necessary"
	@${SYSTEM_PYTHON} -m pip install virtualenv
	@${SYSTEM_PYTHON} -m pip install --upgrade pip

venv:
	@echo "Creating virtual environment"
	@${SYSTEM_PYTHON} -m virtualenv venv

deps:
	@echo "Installing python dependencies"
	@${VENV_PYTHON} -m pip install -r requirements.txt

dev-deps:
	@${VENV_PYTHON} -m pip install honcho wait-for-it pytest

environment: virtualenv venv deps
	@echo "Setting up the python environment"

start:
	@echo "Starting App"
	@${VENV_PYTHON} ${APP_ENTRYPOINT} --mode=normal --verbose --write

emulator: dev-deps
	@echo "Starting Emulator"
	@${VENV_PYTHON} -m honcho start

simulator:
	@${VENV_PYTHON} air_quality --mode=sim --verbose --write

test: dev-deps
	@${VENV_PYTHON} -m pytest tests



.PHONY: virtualenv venv deps environment start emulator simulator test
