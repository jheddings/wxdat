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

build: test
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
	$(PY) $(SRCDIR)/main.py --config $(BASEDIR)/etc/wxdat.yaml

################################################################################
.PHONY: runc

runc: build
	docker container run --rm --tty --publish 9020:9020 \
		--volume "$(PWD):/usr/local/host/pwd" \
		--volume "$(PWD)/etc:/usr/local/host/etc" \
		"$(APPNAME):dev" --config /usr/local/host/etc/wxdat.yaml

################################################################################
.PHONY: rund

rund: release
	docker container run --rm --tty --detach --publish 9020:9020 \
		--volume "$(PWD):/usr/local/host/pwd" \
		--volume "$(PWD)/etc:/usr/local/host/etc" \
		"$(APPNAME):latest" --config /usr/local/host/etc/wxdat.yaml

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
	docker image rm "$(APPNAME):dev"

################################################################################
.PHONY: clobber

clobber: clean
	docker image rm "$(APPNAME):latest"
	docker image rm "$(APPNAME):$(APPVER)"
