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
## MAIN ENTRY

args = parse_args()
conf = load_config(args.config)
monitor = wxdat.Monitor()

# determine global update interval - we are intentionally conservative on the default
if 'update_interval' in conf:
    update_interval = wxdat.parse_duration(conf['update_interval'])
else:
    update_interval = timedelta(minutes=30)

# set up stations from config file
for stat_cfg in conf['stations']:
    stat_labels = stat_cfg.pop('labels', None)
    stat_interval = stat_cfg.pop('update_interval', None)

    # look for a local update interval
    if stat_interval is None:
        stat_interval = update_interval
    else:
        stat_interval = wxdat.parse_duration(stat_interval)

    station = stations.configure(stat_cfg)

    if station is None:
        logger.warning('Could not create monitor for station')
        continue

    station.update_interval = stat_interval
    monitor.add_station(station)

# start the HTTP server
server_port = conf['server_port']
logger.debug('starting metrics server: %d', server_port)
start_http_server(server_port)

# run the metrics collector
logger.info('Server started; starting monitor')
monitor.run()

logger.debug('application exiting')

