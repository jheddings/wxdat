# Makefile for wxdata

BASEDIR ?= $(PWD)
SRCDIR ?= $(BASEDIR)/src

APPNAME ?= $(shell grep -m1 '^name' "$(BASEDIR)/pyproject.toml" | sed -e 's/name.*"\(.*\)"/\1/')
APPVER ?= $(shell grep -m1 '^version' "$(BASEDIR)/pyproject.toml" | sed -e 's/version.*"\(.*\)"/\1/')

VENV := poetry run
PY := $(VENV) python3

################################################################################
.PHONY: all

all: venv build test

################################################################################
.PHONY: build

build: venv test
	poetry --no-interaction build
	docker image build --tag "$(APPNAME):dev" "$(BASEDIR)"

################################################################################
.PHONY: rebuild

rebuild:
	poetry --no-interaction --no-cache build
	docker image build --pull --no-cache --tag "$(APPNAME):dev" "$(BASEDIR)"

################################################################################
.PHONY: release

publish: build test
	## publish PIP package
	poetry publish --no-interaction
	## create docker release tags
	docker image tag "$(APPNAME):dev" "jheddings/$(APPNAME):latest"
	docker image tag "jheddings/$(APPNAME):latest" "jheddings/$(APPNAME):$(APPVER)"
	## publish docker release tags
	docker push "jheddings/$(APPNAME):$(APPVER)"
	docker push "jheddings/$(APPNAME):latest"

################################################################################
.PHONY: run

run: venv
	$(PY) -m wxdat --config $(BASEDIR)/local.yaml

################################################################################
.PHONY: runc

runc:
	docker container run --rm --tty \
		--publish 8077:8077 --volume "$(BASEDIR):/opt/wxdat" \
		"$(APPNAME):dev" --config=/opt/wxdat/local.yaml

################################################################################
.PHONY: test

test:
	$(VENV) pytest $(BASEDIR)/tests --vcr-record=once

################################################################################
.PHONY: venv

venv:
	poetry install

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
