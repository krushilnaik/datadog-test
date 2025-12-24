import requests
from ddtrace import patch_all
from fastapi import FastAPI

patch_all(logging=True)

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [trace_id=%(dd.trace_id)s span_id=%(dd.span_id)s] %(message)s",
)

logger = logging.getLogger(__name__)


app = FastAPI()

USE_CASES = [
    {
        "name": "Weather Lookup",
        "description": "Fetch weather information",
        "mcp_url": "http://localhost:8003/weather",
    },
    {
        "name": "Stock Prices",
        "description": "Get stock price data",
        "mcp_url": "http://localhost:8003/stocks",
    },
]


@app.post("/search")
def search(payload: dict):
    logger.info("Registry searching use cases", extra=payload)

    query = payload["query"].lower()

    for uc in USE_CASES:
        if query in uc["description"].lower():
            logger.info("Use case matched", extra={"use_case": uc["name"]})

            response = requests.post(uc["mcp_url"], json=payload)
            return {"use_case": uc["name"], "result": response.json()}

    logger.warning("No use case found")
    return {"error": "No match"}
