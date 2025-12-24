FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn requests ddtrace langchain langgraph

CMD ["ddtrace-run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
