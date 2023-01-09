# wxdat #

[![PyPI](https://img.shields.io/pypi/v/wxdat.svg)](https://pypi.org/project/wxdat)
[![LICENSE](https://img.shields.io/github/license/jheddings/wxdat)](LICENSE)
[![Style](https://img.shields.io/badge/style-black-black)](https://github.com/ambv/black)

A general purpose weather data recorder & explorer.

## Installation ##

This project uses `poetry` to manage dependencies and a local virtual environment.  To
get started, simply install the dependencies and project with the following:

    poetry install

Alternatively, install the published package using pip:

    pip3 install wxdat

## Usage ##

Simply run the script and tell it which config file to use.

    python3 -m wxdat --config wxdat.yaml

If you are using `poetry` to manage the virtual environment, use the following:

    poetry run python -m wxdat --config wxdat.yaml

## Configuration ##

The configuration file is a YAML document with a list of stations to export.  See the
included default file for more details.

All stations have the following configuration values:
* name - must be unique
* type - the support station type

## Supported Stations ##

Eventually, I'd like to add local stations, not just online sources.  Please see
the example configuration file for details on each provider.

* AccuWeather
* Ambient Weather Network
* OpenWeatherMap
* National Weather Service (NOAA)
* Weather Underground
