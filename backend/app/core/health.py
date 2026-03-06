import asyncio
from typing import Dict, Any, Callable, Awaitable, Optional
from datetime import datetime, timedelta, timezone
from enum import Enum
from sqlalchemy import text
from backend.app.core.db import async_session
from backend.app.core.celery_app import celery_app
from backend.app.core.logging import get_logger

logger = get_logger()

class ServiceStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    STARTING = "starting"
    DOWN = "down"

class HealthCheck:
    def __init__(self):
        self._services: Dict[str, ServiceStatus] = {}
        self._check_function: Dict[str, Callable[[], Awaitable[bool]]] = {}
        self._last_check: Dict[str, datetime] = {}
        self._timeout: Dict[str, float] = {}
        self._retry_delays: Dict[str, float] = {}
        self._max_retries: Dict[str, int] = {}
        self._lock = asyncio.Lock()
        self._dependencies: Dict[str, set[str]] = {}
        self._cache_duration: timedelta = timedelta(seconds=25)
        self._cached_status: Optional[Dict[str, Any]] = None
        self._last_check_time: Optional[datetime] = None

    async def validate_dependencies(self, service_name: str, depends_on: list[str]):
        if not depends_on: 
            return
        
        for dep in depends_on:
            if dep not in self._services:
                raise ValueError(f"Dependency '{dep}' not registered for service '{service_name}'")
