from typing import TypedDict

import requests
from fastapi import FastAPI
from langgraph.graph import END, StateGraph
from logger.logger import logger

app = FastAPI()


class AgentState(TypedDict):
    message: str


def classify(state: AgentState):
    msg = state["message"].lower()
    logger.info("Agent classifying message", extra={"user_message": msg})

    if msg in {"hi", "hello", "hey"}:
        return {"route": "greeting"}

    return {"route": "intent"}


def greeting(state: AgentState):
    logger.info("Greeting detected")
    return {"response": "Hello!"}


def intent(state: AgentState):
    logger.info("Intent detected, calling registry")
    res = requests.post("http://registry:8000/search", json={"query": state["message"]})
    return {"response": res.json()}


builder = StateGraph(AgentState)

builder.add_node("classify", classify)
builder.add_node("greeting", greeting)
builder.add_node("intent", intent)

builder.add_conditional_edges(
    "classify",
    lambda s: s["route"],
    {
        "greeting": "greeting",
        "intent": "intent",
    },
)

builder.add_edge("greeting", END)
builder.add_edge("intent", END)

builder.set_entry_point("classify")

graph = builder.compile()


@app.post("/agent")
def agent(payload: dict):
    logger.info("Agent received request")
    return graph.invoke({"message": payload["message"]})
