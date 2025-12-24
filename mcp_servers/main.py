import logging

from ddtrace import patch_all
from fastapi import FastAPI

patch_all(logging=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [trace_id=%(dd.trace_id)s span_id=%(dd.span_id)s] %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/weather")
def weather(payload: dict):
    logger.info("MCP weather called")
    return {"forecast": "Sunny"}


@app.post("/stocks")
def stocks(payload: dict):
    return {"symbol": "AAPL", "price": 189.32}
