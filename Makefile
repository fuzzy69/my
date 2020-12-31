PROJECT_PATH = $(shell pwd)
PROJECT_NAME = $(shell basename $$PWD)
SOURCES_PATH = $(PROJECT_PATH)/$(PROJECT_NAME)
SCRIPTS_PATH = $(PROJECT_PATH)/scripts
EXPORT_PATH = /mnt/ramdisk/

VERSION = $(shell python3 $(SOURCES_PATH)/version.py)


.PHONY: lint

help:
	@echo "clean  - remove Python file artifacts"
	@echo "format - run code formatter"
	@echo "lint   - check style with flake8"
	@echo "tests  - run unittests"
	@echo "setup  - setup application"

setup:
	virtualenv -p python3 env
	. env/bin/activate && pip install -r requirements.txt && pip install flake8 black

clean:
	find $(SOURCES_PATH) | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rfv
	find $(SOURCES_PATH)/logs/ | grep -E "(\.log|\.err)" | xargs -d '\n' rm -rfv
	find $(SOURCES_PATH)/results/ | grep -E "(\.csv|\.xlsx)" | xargs -d '\n' rm -rfv

unittest:
	python -m unittest discover tests -v

lint:
	flake8 --exclude .git,__pycache__,env,_ > _/lint.log

pack:
	rsync -arv --exclude-from '$(PROJECT_PATH)/_/rsync-exclude.txt' $(SOURCES_PATH) /mnt/ramdisk/
	cd $(EXPORT_PATH) && zip -r -3 $(PROJECT_NAME)_$(VERSION).zip $(PROJECT_NAME)

pip_upgrade:
	pip install --upgrade pip

format:
	black $(SOURCES_PATH)

version:
	python3 $(SCRIPTS_PATH)/make_version.py
