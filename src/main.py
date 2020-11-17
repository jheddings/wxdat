# prometheus client for weather data

import os
import logging

from datetime import timedelta
from prometheus_client import start_http_server

import wxdat
import stations

logger = logging.getLogger('wxdat.main')

################################################################################
def parse_args():
    import argparse

    argp = argparse.ArgumentParser(description='brewdat: homebrew metrics endpoint for prometheus')

    argp.add_argument('--config', default='/etc/brewdat.yaml',
                       help='configuration file (default: /etc/brewdat.yaml)')

    return argp.parse_args()

################################################################################
def load_config(config_file):
    import yaml
    import logging.config

    try:
        from yaml import CLoader as YamlLoader
    except ImportError:
        from yaml import Loader as YamlLoader

    if not os.path.exists(config_file):
        logger.warning('config file does not exist: %s', config_file)
        return None

    with open(config_file, 'r') as fp:
        conf = yaml.load(fp, Loader=YamlLoader)

        if 'logging' in conf:
            logging.config.dictConfig(conf['logging'])

        logger.debug('config file loaded: %s', config_file)

    return conf

################################################################################
def start_metrics_server(conf):
    # start the HTTP server
    server_port = conf.get('server_port', 9022)
    logger.debug('starting metrics server: %d', server_port)

    # the metrics server runs as a background thread; this is non-blocking
    start_http_server(server_port)

################################################################################
## MAIN ENTRY

args = parse_args()
gconf = load_config(args.config)
monitor = wxdat.Monitor()

# set up stations from config file
for station_conf in gconf['stations']:
    station = stations.configure(station_conf, gconf)

    if station is None:
        logger.warning('Unable to create station')
    else:
        monitor.add_station(station)

# start the metrics server after stations are configured
start_metrics_server(gconf)

# run the metrics collector; this method blocks until the application exits
logger.info('starting monitor')
monitor.run()

logger.debug('application exiting')
