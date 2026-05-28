import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler


class AppLogger:
    """
    Production-grade logger class.

    Features:
    - Console logging
    - File logging
    - Error-only file logging
    - Log rotation
    - Environment-based log level
    - Prevents duplicate handlers
    """

    _loggers = {}

    def __init__(
        self,
        name: str = "app",
        log_dir: str = "logs",
        log_file: str = "app.log",
        error_file: str = "error.log",
        max_bytes: int = 5 * 1024 * 1024,
        backup_count: int = 5,
    ):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_file = log_file
        self.error_file = error_file
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()

        self.log_dir.mkdir(parents=True, exist_ok=True)

    def get_logger(self) -> logging.Logger:
        if self.name in AppLogger._loggers:
            return AppLogger._loggers[self.name]

        logger = logging.getLogger(self.name)
        logger.setLevel(self.log_level)
        logger.propagate = False

        if not logger.handlers:
            logger.addHandler(self._console_handler())
            logger.addHandler(self._file_handler())
            logger.addHandler(self._error_file_handler())

        AppLogger._loggers[self.name] = logger
        return logger

    def _formatter(self) -> logging.Formatter:
        return logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | "
                "%(filename)s:%(lineno)d | %(funcName)s() | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    def _console_handler(self) -> logging.Handler:
        handler = logging.StreamHandler()
        handler.setLevel(self.log_level)
        handler.setFormatter(self._formatter())
        return handler

    def _file_handler(self) -> logging.Handler:
        handler = RotatingFileHandler(
            filename=self.log_dir / self.log_file,
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
            encoding="utf-8",
        )
        handler.setLevel(self.log_level)
        handler.setFormatter(self._formatter())
        return handler

    def _error_file_handler(self) -> logging.Handler:
        handler = RotatingFileHandler(
            filename=self.log_dir / self.error_file,
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
            encoding="utf-8",
        )
        handler.setLevel(logging.ERROR)
        handler.setFormatter(self._formatter())
        return handler

# app/core/api_logger.py

import uuid
import json
import socket
import traceback
import requests
from datetime import datetime, timezone



# =============================================================================
# Custom Logger Class
# =============================================================================
import uuid
import json
import socket
import threading
import traceback
import requests
from datetime import datetime, timezone


class ApiLogger:
    def __init__(
        self,
        api_url: str = "https://vibeappop.saa.ai/EnterpriseLogging/api/logs",
        source_application: str = "SectionGeneratorAPI",
        environment: str = "DEV"
    ):
        self.api_url = api_url
        self.source_application = source_application
        self.environment = environment
        self.machine_name = socket.gethostname()

    def log(
        self,
        message: str,
        log_level: int,
        event_type: str,
        source_module: str,
        metadata: dict = None,
        payload: dict = None,
        duration_ms: int = 0,
        is_success: bool = True,
        exception: Exception = None,
        stack_trace: str = None,
        user_id: str = None,
        session_id: str = None,
        correlation_id: str = None,
        request_id: str = None
    ):
        metadata = metadata or {}

        log_payload = {
            "logId": str(uuid.uuid4()),
            "timestampUtc": datetime.now(timezone.utc).isoformat(),
            "logLevel": log_level,
            "message": message,
            "eventType": event_type,
            "sourceApplication": self.source_application,
            "sourceModule": source_module,
            "environment": self.environment,

            "userId": user_id or metadata.get("user_id") or metadata.get("created_by"),
            "sessionId": session_id or metadata.get("session_id"),
            "correlationId": correlation_id or metadata.get("correlation_id"),
            "requestId": request_id or metadata.get("request_id"),

            "machineName": self.machine_name,
            "threadId": str(threading.get_ident()),

            "exceptionMessage": str(exception) if exception else None,
            "stackTrace": stack_trace if stack_trace else traceback.format_exc() if exception else None,

            "metadata": metadata,
            "durationMs": duration_ms,
            "isSuccess": is_success,
            "payloadJson": json.dumps(payload, default=str) if payload else None
        }

        try:
            response = requests.post(
                self.api_url,
                json=log_payload,
                timeout=5
            )
            response.raise_for_status()

        except Exception as log_error:
            # Never break your main app because logging failed
            print(f"Logging API failed: {log_error}")

    def info(
        self,
        message: str,
        event_type: str,
        source_module: str,
        metadata: dict = None,
        payload: dict = None,
        duration_ms: int = 0
    ):
        self.log(
            message=message,
            log_level=1,
            event_type=event_type,
            source_module=source_module,
            metadata=metadata,
            payload=payload,
            duration_ms=duration_ms,
            is_success=True
        )

    def warning(
        self,
        message: str,
        event_type: str,
        source_module: str,
        metadata: dict = None,
        payload: dict = None,
        duration_ms: int = 0
    ):
        self.log(
            message=message,
            log_level=2,
            event_type=event_type,
            source_module=source_module,
            metadata=metadata,
            payload=payload,
            duration_ms=duration_ms,
            is_success=True
        )

    def error(
        self,
        message: str,
        event_type: str,
        source_module: str,
        metadata: dict = None,
        payload: dict = None,
        duration_ms: int = 0,
        exception: Exception = None,
        stack_trace: str = None
    ):
        self.log(
            message=message,
            log_level=3,
            event_type=event_type,
            source_module=source_module,
            metadata=metadata,
            payload=payload,
            duration_ms=duration_ms,
            is_success=False,
            exception=exception,
            stack_trace=stack_trace
        )