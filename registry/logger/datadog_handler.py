import json
import logging
import os
import time
from queue import Queue
from threading import Event, Thread

import requests
from ddtrace.trace import tracer


class DatadogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("DD_API_KEY", "")
        self.service_name = os.getenv("DD_SERVICE", "")
        self.url = "https://http-intake.logs.datadoghq.com/v1/input"
        self.batch_size = 10
        self.flush_interval = 5

        self.queue = Queue()
        self.stop_event = Event()
        self.worker_thread = Thread(target=self._worker, daemon=True)
        self.worker_thread.start()

    def emit(self, record):  # type: ignore
        # get the current tracing context
        span = tracer.current_span()

        log_entry = {
            "message": self.format(record),
            "ddsource": "python",
            "service": self.service_name,
            "level": record.levelname,
            "timestamp": int(record.created * 1000),
        }

        if span:
            log_entry["dd.trace_id"] = str(span.trace_id)
            log_entry["dd.span_id"] = str(span.span_id)

        # Add exception info if present
        if record.exc_info and record.exc_info[0]:
            log_entry["error"] = {
                "kind": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "stack": self.formatter.formatException(record.exc_info) if self.formatter else "",
            }

        # Extract extra fields from the log record
        # Standard LogRecord attributes that we want to skip
        reserved_attrs = {
            "name",
            "msg",
            "args",
            "created",
            "filename",
            "funcName",
            "levelname",
            "levelno",
            "lineno",
            "module",
            "msecs",
            "message",
            "pathname",
            "process",
            "processName",
            "relativeCreated",
            "thread",
            "threadName",
            "exc_info",
            "exc_text",
            "stack_info",
            "taskName",
        }

        # Add any extra fields that aren't standard LogRecord attributes
        extra_fields = {}
        for key, value in record.__dict__.items():
            if key not in reserved_attrs and not key.startswith("_"):
                extra_fields[key] = value

        # Merge extra fields into the log entry
        if extra_fields:
            log_entry.update(extra_fields)
        self.queue.put(log_entry)

    def _worker(self):
        batch = []
        last_flush = time.time()

        while not self.stop_event.is_set():
            try:
                # Try to get an item with timeout
                log_entry = self.queue.get(timeout=1)
                batch.append(log_entry)

                # Flush if batch is full or interval exceeded
                if (
                    len(batch) >= self.batch_size
                    or (time.time() - last_flush) >= self.flush_interval
                ):
                    self._flush_batch(batch)
                    batch = []
                    last_flush = time.time()

            except:
                # Timeout - check if we should flush anyway
                if batch and (time.time() - last_flush) >= self.flush_interval:
                    self._flush_batch(batch)
                    batch = []
                    last_flush = time.time()

    def _flush_batch(self, batch):  # type: ignore
        if not batch:
            return

        try:
            headers = {"DD-API-KEY": self.api_key, "Content-Type": "application/json"}
            # Send as array
            requests.post(self.url, data=json.dumps(batch), headers=headers, timeout=5)
        except Exception as e:
            print(f"Failed to send batch to Datadog: {e}")

    def close(self):
        self.stop_event.set()
        self.worker_thread.join()
        super().close()
