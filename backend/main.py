import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logger.logger import logger

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Backend service started")
logger.error("This is a test error log from backend")
logger.warning("This is a test warning log from backend")
logger.debug("This is a test debug log from backend")


@app.post("/message")
def send_message(payload: dict):
    logger.info("Backend received message", extra={"user_message": payload["message"]})

    response = requests.post("http://agent:8000/agent", json=payload)

    logger.info("Backend forwarding response")
    return response.json()
