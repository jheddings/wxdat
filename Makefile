# Makefile for WeatherData

BASEDIR ?= $(PWD)
SRCDIR ?= $(BASEDIR)/src

APPNAME ?= wxdat
APPVER ?= 0.1

PY := PYTHONPATH="$(SRCDIR)" python3

################################################################################
.PHONY: all

all: build

################################################################################
.PHONY: build

build:
	docker image build --tag "$(APPNAME):dev" "$(BASEDIR)"

################################################################################
.PHONY: rebuild

rebuild:
	docker image build --pull --no-cache --tag "$(APPNAME):dev" "$(BASEDIR)"

################################################################################
.PHONY: release

release: build
	docker image tag "$(APPNAME):dev" "$(APPNAME):latest"
	docker image tag "$(APPNAME):latest" "$(APPNAME):$(APPVER)"

################################################################################
.PHONY: runpy

runpy:
	$(PY) $(SRCDIR)/main.py --config $(BASEDIR)/etc/wxday.yaml

################################################################################
.PHONY: runc

runc:
	docker container run --rm --tty --publish 9020:9020 "$(APPNAME):dev"

################################################################################
.PHONY: rund

rund:
	docker container run --rm --tty --detach --publish 9020:9020 "$(APPNAME):latest"

################################################################################
.PHONY: test

# TODO use a container for tests...

test:
	$(PY) -m unittest discover -v -s $(BASEDIR)/test

################################################################################
.PHONY: clean

clean:
	rm -f "$(SRCDIR)/*.pyc"
	rm -Rf "$(SRCDIR)/__pycache__"
	rm -Rf "$(BASEDIR)/__pycache__"

################################################################################
.PHONY: clobber

clobber: clean
	docker image rm --force "$(APPNAME):dev"
	docker image rm --force "$(APPNAME):latest"
