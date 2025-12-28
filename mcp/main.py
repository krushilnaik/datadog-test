from fastapi import FastAPI
from logger.logger import logger

app = FastAPI()


@app.post("/weather")
def weather(payload: dict):
    logger.info("MCP weather called")
    return {"forecast": "Sunny"}


@app.post("/stocks")
def stocks(payload: dict):
    logger.info("MCP stocks called")
    return {"symbol": "AAPL", "price": 189.32}
