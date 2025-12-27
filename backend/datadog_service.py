import json
import logging
import os
import threading

import requests


class DatadogHTTPHandler(logging.Handler):
    def __init__(self):
        super().__init__()

        self.api_key = os.environ["DD_API_KEY"]
        self.service = os.getenv("DD_SERVICE", "unknown-service")
        self.source = os.getenv("DD_SOURCE", "python")
        self.tags = os.getenv("DD_TAGS", "")
        site = os.getenv("DD_SITE", "datadoghq.com")

        self.url = f"https://http-intake.logs.{site}/v1/input"
        self.session = requests.Session()
        self.lock = threading.Lock()

    def emit(self, record):
        try:
            payload = {
                "message": self.format(record),
                "service": self.service,
                "ddsource": self.source,
                "ddtags": self.tags,
                "status": record.levelname.lower(),
                "logger": record.name,
            }

            headers = {
                "Content-Type": "application/json",
                "DD-API-KEY": self.api_key,
            }

            with self.lock:
                self.session.post(
                    self.url,
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=2,
                )
        except Exception:
            self.handleError(record)


dd_handler = DatadogHTTPHandler()

formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
dd_handler.setFormatter(formatter)
