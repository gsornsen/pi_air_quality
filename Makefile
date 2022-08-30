PROJ_DIR="`pwd`"
SYSTEM_PYTHON=python3
VENV_PYTHON="${PROJ_DIR}/venv/bin/python3"
SOURCE_DIR="${PROJ_DIR}"
APP_ENTRYPOINT="${SOURCE_DIR}/app.py"


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
	@${VENV_PYTHON} -m pip install honcho wait-for-it

environment: virtualenv venv deps
	@echo "Setting up the python environment"

start:
	@echo "Starting App"
	@${VENV_PYTHON} ${APP_ENTRYPOINT}

emulator: dev-deps
	@echo "Starting Emulator"
	@${VENV_PYTHON} -m honcho start

simulator:
	@${VENV_PYTHON} src --mode=sim --verbose --write


.PHONY: virtualenv venv deps environment start
