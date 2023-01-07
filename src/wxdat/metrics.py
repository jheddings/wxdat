"""Metrics container class for wxdat."""

import logging

from prometheus_client import Counter, start_http_server

log = logging.getLogger(__name__)


class AppMetrics:
    def __init__(self, port=None):
        standard_labels = ["provider", "station_name"]

        self.client_errors = Counter(
            "client_errors", "API client errors", labelnames=standard_labels
        )
        self.download_errors = Counter(
            "download_errors", "API download errors", labelnames=standard_labels
        )

        self.logger = log.getChild("AppMetrics")

        if port is None:
            self.logger.debug("metrics server NOT started -- no port specified")
        else:
            self.logger.info("Starting metrics server on port: %d", port)
            start_http_server(port)
