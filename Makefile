# Makefile for wxdata

BASEDIR ?= $(PWD)
SRCDIR ?= $(BASEDIR)/src

APPNAME ?= $(shell grep -m1 '^name' "$(BASEDIR)/pyproject.toml" | sed -e 's/name.*"\(.*\)"/\1/')
APPVER ?= $(shell grep -m1 '^version' "$(BASEDIR)/pyproject.toml" | sed -e 's/version.*"\(.*\)"/\1/')

VENV := poetry run
PY := $(VENV) python3

################################################################################
.PHONY: all

all: build

################################################################################
.PHONY: build

build: test
	poetry --no-interaction build
	docker image build --tag "$(APPNAME):dev" "$(BASEDIR)"

################################################################################
.PHONY: rebuild

rebuild:
	poetry --no-interaction --no-cache build
	docker image build --pull --no-cache --tag "$(APPNAME):dev" "$(BASEDIR)"

################################################################################
.PHONY: release

release: build test
	docker image tag "$(APPNAME):dev" "$(APPNAME):latest"
	docker image tag "$(APPNAME):latest" "$(APPNAME):$(APPVER)"

################################################################################
.PHONY: run

run:
	$(PY) -m wxdat --config $(BASEDIR)/local.yaml

################################################################################
.PHONY: runc

runc:
	docker container run --rm --tty --publish 8077:8077 \
		--volume "$(BASEDIR):/opt/wxdat" "$(APPNAME):dev"

################################################################################
.PHONY: test

test:
	$(VENV) pytest $(BASEDIR)/tests --vcr-record=once

################################################################################
.PHONY: clean

clean:
	rm -f "$(BASEDIR)/wxdat.log"
	rm -Rf "$(BASEDIR)/.pytest_cache"
	find "$(BASEDIR)" -name "*.pyc" -print | xargs rm -Rf
	find "$(BASEDIR)" -name '__pycache__' -print | xargs rm -Rf
	docker image rm "$(APPNAME):dev"

################################################################################
.PHONY: clobber

clobber: clean
	rm -Rf "$(BASEDIR)/dist"
	rm -Rf "$(BASEDIR)/.venv"
	docker image rm "$(APPNAME):latest"
	docker image rm "$(APPNAME):$(APPVER)"
