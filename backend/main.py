import logging

import requests
from ddtrace import patch_all
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

patch_all(logging=True)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [trace_id=%(dd.trace_id)s span_id=%(dd.span_id)s] %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/message")
def send_message(payload: dict):
    logger.info("Backend received message", extra={"user_message": payload["message"]})

    response = requests.post("http://agent:8000/agent", json=payload)

    logger.info("Backend forwarding response")
    return response.json()
