# wxdat

A general purpose weather exporter for Prometheus.

## Usage

Simply run the script and tell it which config file to use.

    python3 wxdat.py --config my_wxdat.yaml

## Configuration

The configuration file is a YAML document with a list of stations to export.  See the sample in `etc` for more details.

All stations have the following configuration values:
* name - must be unique
* type - the support station type

## Supported Stations

Eventually, I'd like to add more local stations, not just online sources.

### Dark Sky

Configuration values:
* api_key
* latitude
* longitude

### OpenWeather
* api_key
* latitude
* longitude

### Weather Underground
* api_key
* station_id
