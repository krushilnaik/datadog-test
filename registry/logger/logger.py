import logging

from ddtrace import patch_all

from .datadog_handler import DatadogHandler

patch_all(logging=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [trace_id=%(dd.trace_id)s span_id=%(dd.span_id)s] %(message)s",
)

dd_handler = DatadogHandler()

logger = logging.getLogger(__name__)
logger.addHandler(dd_handler)
